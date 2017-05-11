#!/usr/bin/python
import sys, os, glob, fnmatch, subprocess, markdown



app_home_dir = os.path.normpath(os.path.dirname(sys.argv[0])+"/..")
layout_dir = os.path.join("CodeSource","templates","doc")
style_sheet_path = os.path.join(layout_dir,"stylesheets","stylesheet.css")
_extensions=['markdown.extensions.codehilite','markdown.extensions.fenced_code','markdown.extensions.toc']
_extension_configs = {
    'markdown.extensions.codehilite': {
        'css_class': 'highlight'
     }
}
os.chdir(app_home_dir)

"""
for root,dirs,files,fdroot in os.fwalk(app_home_dir):
    for file_name in fnmatch.filter(files,'*.md'):
        css_link_path=os.path.join(root,file_name)
        print(css_link_path)
"""

file_paths = glob.glob("**/*.md",recursive=True)
for file_path in file_paths :
    css_link_path= ("../"*file_path.count(os.path.sep))+style_sheet_path
    html_file_name = os.path.splitext(file_path)[0]+".html"
    print(html_file_name, css_link_path)
    with open(os.path.join(app_home_dir,layout_dir,"index.html"),'r') as source:
        with open(html_file_name,'wb') as dest:
            for line in source:
                if "{markdown_output}" in line : 
                    markdown.markdownFromFile(file_path,output=dest,extensions=_extensions, extension_configs=_extension_configs)            
                else:
                    output_line = line.replace("{stylesheetpath}",css_link_path)
                    dest.write(output_line.encode('utf-8'))
    

"""
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
