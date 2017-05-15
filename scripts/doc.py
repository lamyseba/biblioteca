#!/usr/bin/python
import sys, os, glob, markdown, re, codecs, argparse, datetime, locale
from string import Template

# récupère et vérifie les arguments de la ligne de commande
parser = argparse.ArgumentParser(description="""
Génère la documentation de la bibliothèque au format html (consultable dans un 
navigateur), à partir de l'ensemble des fichiers d'extension '.md' qui se 
trouvent dans le projet. Les fichiers .md sont des fichiers au format Markdown,
modifiables avec un simple éditeur de texte. Pour plus d'information sur la 
consultation et la modification de la documentation, consultez le fichier 
Documentation/utiliser-la-documentation.html""")


# définit le répertoire de travail: celui juste au dessus de là où
# se trouve ce script
os.chdir(os.path.normpath(os.path.dirname(sys.argv[0])+"/.."))
# app_dir: le répertoire de base de l'application
app_dir = os.getcwd()
# template_dir : là ou se trouve le modèle de page pour la documentation
template_dir = os.path.join(app_dir,"scripts","templates")
# html_dir: là ou seront généré les fichiers html de la documenatation
html_dir = os.path.join(app_dir,"docs","html")

 
# DEPRECATED: on paramètre désormais l'extension toc pour qu'elle
# génère les même ancres que github
#
# Les ancres générées par github peuvent contenir des accents, pas celles
# générées par python_markdown. Donc pour la version locale de la documentation
# (générée avec python_markdown), il faut supprimer les ancres. Aussi, il
# faut pointer vers le ficher html plutôt que le fichier .md
# une expression régulière pour trouver les liens entre parenthèse vers des 
# fichiers .md, avec une ancre dans le lien
# parenthèse. Ex:[impression.py](scripts/README.md#impression.py)
# alp signifie anchor link pattern
alp = re.compile('(\]\s*\(.*)\.md#?([^\)]*)')

# DEPRECATED: idem
#
# Une autre expression, cette fois pour trouver des liens en note.
# Ex: [impression.py]:scripts/Readme.md#impression.py
# Il faut supprimer les accents des ancres dans la version html
alp2 = re.compile('(\]\s*:.*)\.md#?(.*)')

# header pattern
h1p = re.compile('#\s*([^#\n]+)|(.+)\n={5,}')



def slugify(value,separator):
    """ définit une façon de générer les ancres compatible avec github 
    """ 
    output = value.lower()   
    output = re.compile('[^\w\s'+separator+']+').sub('',output)
    output = re.compile('\s+').sub(separator,output)
    return output

md=markdown.Markdown(
    extensions=['markdown.extensions.codehilite',
                'markdown.extensions.fenced_code',
                'markdown.extensions.toc',
                'markdown.extensions.meta'
               ],
    extension_configs = {
        'markdown.extensions.codehilite': {
            'css_class': 'highlight'
        },
        'markdown.extensions.toc': {
            'slugify':slugify
        }
    })


html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
    }

def html_escape(text):
    """ Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)

# pour le
def convert_internal_links(text):
    """ Convertit les lien interne qui pointent vers le répertoire docs dans le 
        texte fournit. Par exemple un lien vers "../docs/index.html" sera 
        transformé en lien vers "index.html". Cette fonction ne sert que pour
        le fichier scripts/README.md, car il ne se trouve pas dans le répertoire
        docs et il est quand même inclut dans la génération de la documentation.
        text -- le texte dans lequel il faut convertir les liens
    """
    return re.compile('(][:\(]).*docs/(.*)\.md').sub(r'\1\2.html',text)


# DEPRECATED: cette fonction ne sert plus à rien dans la nouvelle structure
# de la documentation: on y met directement le lien vers le fichier html,
# et non vers le fichier .md
def ext_and_slug(match):
    """ transforme un lien vers un fichier d'extension `.md` en un lien vers
        le fichier de même nom mais d'extension `.html`. Transforme
        l'ancre du lien pour la rendre compatible avec python-markdown
        (utilisation de la méthode slugify)
        match -- un RegExpMatch contenant le lien.
    """
    modified_link = match.group(1)+".html"
    if match.group(2):
        modified_link += '#'+markdown.extensions.toc.slugify(match.group(2),'-')
    print("link conversion:",match.group(0))
    print("              ->",modified_link)
    return modified_link



# créé le répertoire html s'il n'existe pas
if not os.path.exists(html_dir) : os.makedirs(html_dir)
os.chdir(html_dir)
# créé le lien symbolique vers le répertoire des css s'il n'existe pas
if not os.path.exists('doc-stylesheets'):
    os.symlink("../../scripts/templates/doc-stylesheets",'doc-stylesheets')    
## créé le lien symbolique vers le répertoire images s'il n'existe pas
if not os.path.exists('images'):
    os.symlink("../images","images")
os.chdir(app_dir)

# file_paths: la liste de tous les fichiers .md à convertir en html.
# Le chemin donné pour chaque fichier est relatif au répertoire de travail.
# ex: "./docs/index.md"
# ajoute le fichier "scripts/README.md" en début de liste
file_paths = ["scripts/README.md"]
# ajoute tous les fichiers ".md" du répertoire docs.
file_paths.extend(glob.glob("docs/*.md"))
for file_path in file_paths :
    print("---")
    # md_file_path_abs : chemin absolu vers le fichier markdown
    md_file_path_abs= os.path.join(app_dir,file_path)
    print("rendering "+file_path)
    # file_name : le nom du fichier markdown
    md_file_name = os.path.basename(file_path)
    # html_file_name : le nom du fichier html généré à partir du fichier markdown
    # on change juste l'extension .md en .html
    html_file_name = os.path.splitext(md_file_name)[0]+".html"
    # html_file_path: chemin absolu du fichier html généré
    # on le place dans le sous-répertoire html
    html_file_path = os.path.join(html_dir,html_file_name)
    
    # ouvre le fichier markdown et le lit
    md_in=""
    with open(md_file_path_abs,'r') as f:
        md_in = f.read()
    if file_path=='scripts/README.md':
        md_in = convert_internal_links(md_in)
        html_file_path = os.path.join(html_dir,"utilisation-des-scripts.html")
    # trouve le titre 
    matches=h1p.search(md_in).groups()
    title = matches[0] or matches[1]
    print("#",title)
    # transforme le texte markdown en html
    html_out = md.convert(md_in)
    
    # ouvre le template de documention
    template_in = ""
    with open(os.path.join(template_dir,"doc.html"),'r') as f:
        template_in = f.read()
    template = Template(template_in)    
    
    
    # La chaine de caractère qui précise l'auteur de la page.
    # Ex: Auteur: Sébastien Lamy
    authors = ""
    
    # Pour afficher la date de modification, il faut mattre à jour la localisation
    # de python
    update_time = datetime.datetime.fromtimestamp(os.path.getmtime(md_file_path_abs))
    locale.setlocale(locale.LC_ALL,"fr_FR.UTF-8")    
    for key in md.Meta :
        if key.lower().startswith("auteur") : 
            authors = "; ".join(md.Meta[key])            
            authors = key.title()+"&nbsp;: "+html_escape(authors)
    
    # substitue les champs à substituer
    template_out = template.safe_substitute(
        markdown_output=html_out,
        authors= authors,
        source_file_path = md_file_path_abs,
        update_date = update_time.strftime("%d %b %Y"),
        title=title
    )       
    # crée le fichier html avec le contenu final
    with codecs.open(html_file_path,'w',encoding="utf-8", errors="xmlcharrefreplace") as f:
        f.write(template_out)
    md.reset()
    print()
    

"""
DEPRECATED: tentative de fonctionner avec la commande sed
f=open('/tmp/calandreta_'+self.item_type+'.html','w')
        args=[  'xsltproc',
                '--param','entry_predicate','"'+self.entry_predicate+'"',
                '--param','sort-name1',"'%s'"%sort[self.item_type],
                input_dir+'/'+self.item_type+'.xsl',
                tmp_xml_path    ]
        logging.debug(" ".join(args))
        subprocess.check_call(args,stdout=f)
        f.close()

sed -e 's/{markdown_output}/markdown '+file+'/e' Documentation/template/documentation.html>Documentation/index.html

"""
