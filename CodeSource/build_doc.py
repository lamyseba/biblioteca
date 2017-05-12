#!/usr/bin/python
import sys, os, glob, markdown, re, codecs
from string import Template


# définit le répertoire de travail: celui juste au dessus de là où
# se trouve ce script
os.chdir(os.path.normpath(os.path.dirname(sys.argv[0])+"/.."))
layout_dir = os.path.join("CodeSource","templates","doc")
style_sheet_path = os.path.join(layout_dir,"stylesheets","stylesheet.css")
md=markdown.Markdown(
    extensions=['markdown.extensions.codehilite',
                'markdown.extensions.fenced_code',
                'markdown.extensions.toc'
               ],
    extension_configs = {
        'markdown.extensions.codehilite': {
            'css_class': 'highlight'
        }
    })


def ext_and_slug(match):
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
alp2 =re.compile('(\]\s*:.*)\.md#?(.*)')



# file_paths: la liste de tous les chemin des fichiers .md, relatif au
# répertoire de travail.
file_paths = glob.glob("**/*.md",recursive=True)
for file_path in file_paths :
    print("---")
    # on calcule l'emplacement du fichier de mise en forme en fonction
    # du chemin du fichier .md
    css_link= ("../"*file_path.count(os.path.sep))+style_sheet_path
    html_file_name = os.path.splitext(file_path)[0]+".html"
    print("rendering "+file_path)
    
    # ouvre le fichier markdown
    md_in=""
    with open(os.path.join(os.getcwd(),file_path),'r') as f:
        md_in = f.read()    
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
    template_out = template.substitute(
        markdown_output=html_out,
        css_link=css_link
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
