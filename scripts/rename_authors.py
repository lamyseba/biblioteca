#!/usr/bin/python3
# coding: utf-8
import os, subprocess, sys, argparse
import xml.etree.ElementTree as ET

# récupère et vérifie les arguments de la ligne de commande
parser = argparse.ArgumentParser(description="""
Ce script permet de renommer tous les auteurs de la base Tellico: Tous les
auteurs saisis sous la forme "Dupont, Jean" deviendront: "Jean Dupont".""",
epilog="""
---
Avantages : cette nouvelle mise en forme des auteurs simplifie la saisie: on 
copie tel quel ce qui est indiqué sur le livre
---
Inconvénient: Dans certains cas, l'auto-complétion de l'auteur disfonctionne:
    * Pour les auteurs dont le prénom n'est pas fourni sur certains livres    
    * Pour les auteurs dont seule l'initiale du prénom est fournie sur le livre    
    * Pour les couples (deux prénoms et un seul nom)
---
Plus d'éléments sur le choix du formatage des noms d'auteurs dans le fichier 
"Documentation/format_noms_d_auteur"
""", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("input_file",type=str,help='le fichier de base de donnée tellico à transformer')
parser.add_argument("output_file",type=str,help="le nom du fichier de sortie", default="output.tc")
parser.add_argument("-v","--verbose",help="affiche les transformations de nom sur la sortie standard", action="store_true")
args = parser.parse_args()
if not os.path.exists(args.input_file):
    print("Je ne trouve pas le fichier: "+args.input_file)
    exit()

# L'emplacement de la copie temporaire de la base de donnée Tellico
tmp_xml_path = "/tmp/tellico.xml"

# initialise des variable utiles pour la lecture du fichier base de donnée tellico
# (au format xml)
ns = {'tc': 'http://periapsis.org/tellico/'}

# Dézippe le fichier de la liste des livres (cette sauvegarde est au format xml)
subprocess.call(['unzip','-o',args.input_file,'tellico.xml','-d','/tmp'])
# tellico_xml -- Le fichier xml de la base de donnée tellico
tellico_xml = ET.parse(tmp_xml_path)
# authors -- les auteurs
authors = tellico_xml.iterfind('.//tc:author',ns)

author_updates=[]
for author in authors:
    names=author.text.split(",")
    names.reverse()
    new_name = " ".join(names).strip()
    # liste la modification si on veut une sortie bavarde
    if args.verbose: author_updates.append(author.text+"->"+new_name)
    author.text=new_name
# Sortie bavarde: Affiche une liste des auteurs et la transformation appliquée. 
# La liste est triée par ordre alphabêtique
for update in sorted(list(set(author_updates))): print(update)

# Enregistre le fichier xml temporaire avec le modifications
with open(tmp_xml_path, 'wb') as f:
    f.write(bytes(
        '<?xml version="1.0" encoding="UTF-8" ?>\n'+
        "<!DOCTYPE tellico PUBLIC '-//Robby Stephenson/DTD Tellico V11.0//EN' 'http://periapsis.org/tellico/dtd/v11/tellico.dtd'>\n",
        'utf-8'))
    tellico_xml.write(f,'utf-8')
    
# Copie le fichier xml temporaire dans une nouvelle base de données tellico
subprocess.call(["zip","-r","-j",args.output_file,tmp_xml_path])
print("Base de donnée avec les nouveaux noms d'auteur : "+args.output_file)

