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
layout_dir = os.path.join("CodeSource","templates","doc")
style_sheet_path = os.path.join(layout_dir,"stylesheets","stylesheet.css")
md=markdown.Markdown(
    extensions=['markdown.extensions.codehilite',
                'markdown.extensions.fenced_code',
                'markdown.extensions.toc',
                'markdown.extensions.meta'
               ],
    extension_configs = {
        'markdown.extensions.codehilite': {
            'css_class': 'highlight'
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
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)


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

 
# Les ancres générées par github peuvent contenir des accents, pas celles
# générées par python_markdown. Donc pour la version locale de la documentation
# (générée avec python_markdown), il faut supprimer les ancres. Aussi, il
# faut pointer vers le ficher html plutôt que le fichier .md
# une expression régulière pour trouver les liens entre parenthèse vers des 
# fichiers .md, avec une ancre dans le lien
# parenthèse. Ex:[impression.py](CodeSource/README.md#impression.py)
# alp signifie anchor link pattern
alp = re.compile('(\]\s*\(.*)\.md#?([^\)]*)')

# Une autre expression, cette fois pour trouver des liens en note.
# Ex: [impression.py]:CodeSource/Readme.md#impression.py
# Il faut supprimer les accents des ancres dans la version html
alp2 = re.compile('(\]\s*:.*)\.md#?(.*)')

# header pattern
h1p = re.compile('#\s*([^#\n]+)|(.+)\n={5,}')


# file_paths: la liste de tous les chemin des fichiers .md, relatif au
# répertoire de travail.
file_paths = glob.glob("**/*.md",recursive=True)
for file_path in file_paths :
    print("---")
    # on calcule l'emplacement du fichier de mise en forme en fonction
    # du chemin du fichier .md
    home_path_rel = ("../"*file_path.count(os.path.sep))
    css_link= os.path.normpath(home_path_rel+style_sheet_path)
    html_file_name = os.path.splitext(file_path)[0]+".html"
    print("rendering "+file_path)
    
    md_in=""
    # file_path_abs : chemin absolu vers le fichier markdown
    file_path_abs= os.path.join(os.getcwd(),file_path)
    # ouvre le fichier markdown
    with open(file_path_abs,'r') as f:
        md_in = f.read()    
    # trouve le titre 
    matches=h1p.search(md_in).groups()
    title = matches[0] or matches[1]
    print("#",title)
    # transforme les ancres dans le fichier markdown 
    md_out=alp.sub(ext_and_slug,md_in)
    md_out=alp2.sub(ext_and_slug, md_out) 
    # transforme le texte markdown en html
    html_out = md.convert(md_out)
    
    # ouvre le template de documention
    template_in = ""
    with open(os.path.join(os.getcwd(),layout_dir,"index.html"),'r') as f:
        template_in = f.read()
    template = Template(template_in)
    # substitue les champs à substituer
    
    # La chaine de caractère qui précise l'auteur de la page.
    # Ex: Auteur: Sébastien Lamy
    authors = ""
    
    # Pour afficher la date de modification, il faut mattre à jour la localisation
    # de python
    update_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path_abs))
    locale.setlocale(locale.LC_ALL,"fr_FR.UTF-8")
    
    for key in md.Meta :
        if key.lower().startswith("auteur") : 
            authors = "; ".join(md.Meta[key])            
            authors = key.title()+"&nbsp;: "+html_escape(authors)
    template_out = template.safe_substitute(
        markdown_output=html_out,
        css_link=css_link,
        summary_link=os.path.normpath(home_path_rel+"README.html"),
        authors= authors,
        source_file_path = file_path_abs,
        update_date = update_time.strftime("%d %b %Y"),
        edit_man_url= os.path.normpath(home_path_rel+"Documentation/utiliser-la-documentation.html"),
        title=title
    )       
    # crée le fichier html avec le contenu final
    with codecs.open(html_file_name,'w',encoding="utf-8", errors="xmlcharrefreplace") as f:
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
