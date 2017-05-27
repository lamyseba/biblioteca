#!/usr/bin/python3
# coding: utf-8
import argparse, dbus, os, subprocess, sys, time, logging, re
import xml.etree.ElementTree as ET
from datetime import datetime

description="""
Un automate pour imprimer les fiches et les cotes des livres qui en ont besoin. 
Ce programme génère un pdf et met à jour le fichier d'inventaire: il remet à 
zéro le nombre de fiche ou de cote à imprimer pour les livres concernés.

Ce script peut être lancé en ligne de commande depuis un terminal. On peut
aussi cliquer sur les lanceurs `Impression des fiches` et `Impression des cotes` 
à la racine du projet pour exécuter ce script sans option.

Le fichier pdf est stocké dans le répertoire `impressions/fiches` ou
`impressions/cotes` à la racine du projet. La liste des livres traités lors
de chaque exécution du script est écrite à la fin du fichier 
`impressions/impression.log`.

La mise à jour des données est déléguée à Tellico si Tellico est 
ouvert, sinon ce script met à jour directement le fichier `inventaire.tc` où 
sont sauvegardées les données.

Le premier argument indique s`il faut imprimer les fiches ou les cotes : Ce 
script ne fait pas les deux à la fois.
"""

epilog="""
Exemples d'utilisation:
# Imprime toutes les fiches manquantes
impression.py fiches 

# Imprime les cotes manquantes de tous les livres qui ne sont pas du 
# genre "Documentaire"
impression.py cotes --exclude Documentaire 

# Imprime toutes les fiches manquantes et détaille le déroulé sur la sortie 
# standard (au lieu de l'écrire dans le fichier de log)
impression.py fiches --log debug

"""

# Le répertoire de base de l'application est le répertoire parent de l'emplacement
# du script 
app_home_dir = os.path.normpath(os.path.dirname(sys.argv[0])+"/..")

# Le chemin qui pointe sur le fichier de base de donnée de Tellico
# (format xml zippé)
tellico_file_path = os.path.join(app_home_dir,"inventaire.tc")

# Le répertoire dans lequel seront enregistré les pdf à imprimer
output_dir=os.path.join(app_home_dir,'impressions')

# L'emplacement du fichier de log
logfile_path=os.path.join(output_dir,"impression.log")

# Le répertoire dans lequel se trouvent les templates xsl 
input_dir=os.path.join(app_home_dir,'scripts','templates')

# L'emplacement de la copie temporaire de la base de donnée Tellico
tmp_xml_path = "/tmp/tellico.xml"

# L'emplacement du fichier qui liste les correspondance code-mot clé pour
# les cotes des documentaires
docu_codes_path = os.path.join(app_home_dir, 'docs/sources/cotes_documentaires.md')

# Le tri souhaité pour l'impression
sort={"fiches":"ID","cotes":"cote"}

# Les options d'impression du html en pdf
wk_options={
    "fiches":['-s','A4','-B','8mm','-T','8mm','-L','8mm','-R','8mm','-O','Landscape','--disable-smart-shrinking'],
    "cotes": ['-s','A4','-B','11mm','-T','11mm','-L','5mm','-R','5mm','--disable-smart-shrinking']}

# Le nom du champs de base de donnée qui précise le nombre de fiche
# ou de cote à imprimer pour un livre
print_count_db_name={
    "fiches":"cards-miss-count",
    "cotes":"shelf-nums-miss-count"}

# initialise des variable utiles pour la lecture du fichier base de donnée tellico
# (au format xml)
ns = {'tc': 'http://periapsis.org/tellico/'}
ET.register_namespace('','http://periapsis.org/tellico/')

# la liste des genres à exclure
excluded_genres=[]


# récupère et vérifie les arguments de la ligne de commande
parser = argparse.ArgumentParser(
    description=description,
    epilog=epilog,
    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("item_type",type=str,help="peut prendre la valeur 'fiches' ou 'cotes'")
parser.add_argument("--log",type=str,help="info or debug", default="info")
parser.add_argument("--exclude",type=str,help="la liste des genres à exclure, séparés par des ';'")
args = parser.parse_args()

# Le type d'item qu'on imprime (fiches ou cotes)
if args.item_type!="fiches" and args.item_type!="cotes":
    raise ValueError("L'argument doit être 'fiches' ou 'cotes', pas %s" % args.item_type)

# Récupère les genre à exclure
if args.exclude is not None: excluded_genres=args.exclude.split(";")

#Initialise le logger
# il faut un répertoire "impressions" pour pouvoir logger
if not os.path.exists(output_dir): os.makedirs(output_dir)
log_level = getattr(logging, args.log.upper(), None)
if not isinstance(log_level, int):
    raise ValueError('Invalid log level: %s' % args.log)

if log_level == logging.DEBUG: 
    logfile_path=None
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=log_level,
                    filename=logfile_path)


# Vérifie si tellico est lancé
bus = dbus.SessionBus()
tellico_is_launched = False
if "org.kde.tellico" in bus.list_names(): 
    tellico_is_launched = True
    dbus_collection = bus.get_object("org.kde.tellico", "/Collections")
    
def shell_command(args,debug=True,check=True):
    """ lance une commande shell et affiche le debug """
    if debug: logging.debug(" ".join(args))
    if check: subprocess.check_call(args)
    else: subprocess.call(args)

def open_path(path):
    """ lance l'emplacement choisi avec l'application par défaut
        path -- l'emplacement choisi
    """
    # si on est sous linux
    if sys.platform.startswith('linux'):
        logging.debug("showing the pdf file for user")
        subprocess.call(['xdg-open', path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                 # on capture stdin et out pour rendre le 
                                 # tout non bloquant 
    
class Item:
    def xml_value(self,field_name):
        """ Consulte le xml pour renvoyer le texte d'un champs simple 
            (comme le titre ou la cote) pour le livre correspondant à cet item
        """
        xml_node = self.xml_entry.find("tc:"+field_name,ns)
        if xml_node is not None: return xml_node.text
        else: return None
        
    def __init__(self,xml_entry,item_type):        
        # le noeud xml de la base de donnée tellico qui correspond à cet item
        self.xml_entry=xml_entry
        
        # type: fiches ou cotes
        self.item_type=item_type
        
        # print_count: le nombre de fois ou on doit imprimer cet item
        self.print_count=0        
        xml_print_count=self.xml_value(print_count_db_name[item_type])
        if xml_print_count is not None: self.print_count = int(xml_print_count)        
        
        # xml_id: l'id du noeud xml qui correspond à cet item        
        self.xml_id = int(self.xml_entry.attrib["id"])        
        
        # xml_cote: la cote du livre qui correspond à cet item        
        self.xml_cote = self.xml_value("cote")
        
        # xml_genre: le genre du livre qui correspond à cet item        
        self.xml_genre = self.xml_value("genre")
                
        # shall_be_printed: doit on imprimer cet item ou pas?
        # Cet attribut doit avoir la même logique que le entry_predicate du PrintManager
        self.shall_be_printed=False        
            ## le nombre d'exemplaire à imprimer doit être positif
            ## la cote ne doit pas être vide
            #le genre ne doit pas être exclu
                    
        
        if      self.print_count>0 \
                and self.xml_cote is not None  \
                and self.xml_genre not in excluded_genres:
            self.shall_be_printed=True                        
            # des variables pour le log
            xml_title = self.xml_value("title")
            xml_cote = str.replace(self.xml_cote,"\n",' ')
                
            if item_type=="fiches":
                logging.info("%i fiche(s) pour le livre %i %s - %s",
                            self.print_count,self.xml_id,xml_cote,xml_title)

            if item_type=="cotes": 
                logging.info("%i cote(s) pour le livre %i %s- %s",
                            self.print_count,self.xml_id,xml_cote,xml_title)
            
            
    def update_tellico(self,field_name,value):
        """ met à jour un champs simple (sans valeurs multiple possible), pour le livre
        qui correspond à cet item (fiche ou cote)
        field_name -- le nom du champs à mettre à jour dans tellico
        value -- la valeur qu'on veut attribuer au champs
        """
        # Si tellico est ouvert, on lui demande de faire la mise à jour
        if tellico_is_launched:
            dbus_collection.setEntryValue(self.xml_id,field_name,value)
        # sinon on met à jour directement dans le fichier de base de donnée de tellico)
        else:
            xml_node = self.xml_entry.find("tc:"+field_name,ns)
            if  xml_node is None: xml_node=ET.SubElement(self.xml_entry,field_name)
            xml_node.text=value
     
    def clear_print_count(self):
        """ met à zéro le nombre d'impression nécessaire pour cet item (fiche ou cote),
            et met tellico à jour en consequence
        """
        logging.debug("clearing print count on %s for entry %i",self.item_type,self.xml_id)
        self.update_tellico(print_count_db_name[self.item_type],"0")
        self.print_count=0
    
        

class PrintManager:
    def _init_tellico_xml(self):
        # Si tellico n'est pas lancé et qu'un xml temporaire existe déjà, 
        # on attend que le xml temporaire soit supprimé (un autre programme est 
        # en train de l'utiliser pour mettre à jour la base de donnée tellico)
        if not tellico_is_launched:
            nb_sec=0            
            while os.path.exists(tmp_xml_path) and nb_sec <= 3 :
                logging.debug("tellico xml database is locked, waiting...")
                # Attend 5 secondes max
                time.sleep(1)
                nb_sec+=1
        # Enregistre le lancement de l'impression dans le fichier de log
        logging.info("")
        logging.info("===============================================")
        logging.info("Lancement de l'impression des "+self.item_type)
        logging.info("===============================================")        
        if tellico_is_launched:
            logging.info("Le programme Tellico est ouvert, il sera utilisé pour mettre à jour es données d'impression")
        else:
            logging.info("Le programme Tellico est fermé, la mise a jour des données d'impression se fera dans son fichier de sauvegarde")
        if os.path.exists(tmp_xml_path):
            logging.warning("Le fichier de sauvegarde est resté vérouillé trop longtemps, vérouillage ignoré")
        # Enregistre un marqueur temps avant de dezipper le fichier xml
        self.start = time.time()
        # Dézippe le fichier de la liste des livres (cette sauvegarde est au format xml)
        shell_command(['unzip','-o',tellico_file_path,'tellico.xml','-d','/tmp'])
        # Récupère le xml des données
        return ET.parse(tmp_xml_path)
        
        
    def _init_docu_codes(self):
        """ Lit le fichier qui contient la liste des codes de documentaire et
            leur traduction en mot clé. Génère un fichier xml temporaire
            qui contient ces informations. La fabrication du html à partir
            du template xslt et des données tellico utilisera ce fichier pour
            ajouter le mot clé à côté du code numérique
        """        
        # On ne fait ce travail que pour les cotes, car les mots-clés ne sont
        # pas affiché sur les fiches
        if self.item_type != "cotes":  return
        
        # L'endroit ou est stocké le fichier temporaire. Cet endroit doit
        # correspondre à celui précisé dans le template cotes.xslt
        docu_codes_xml_path = "/tmp/codes.xml"
        logging.debug("translating docu codes from %s to %s", docu_codes_path, docu_codes_xml_path)
        # On construit des noeuds xml pour chaque cotes. La structure est
        # du type
        # <cotes>
        #   <cote id="100">Psychologie</cote>
        #   <cote id ="...">...</cote>
        #   ...
        # </cotes>
        codes = ET.Element('cotes')
        codes_xml=ET.ElementTree(codes)
        content=""
        # L'expression régulière pour trouver les titres qui nous intéressent 
        # dans le fichier source: précédé par ### ou d'un début de ligne, 
        # commence par 3 chiffres puis ":", est suivi de "<!--" ou d'une fin 
        # de ligne.
        p=re.compile(r'#{0,3}\s*(\d{3})\s*:(.*?)((<!--)|$)',re.M)
        with open (docu_codes_path,'r') as f:
            content=f.read()
        for code_match in p.finditer(content):
            code=ET.SubElement(codes,'cote')
            code.set('id',code_match.group(1))
            code.text=code_match.group(2).strip()
        codes_xml.write(docu_codes_xml_path,encoding='utf-8')
    
    def _validate_excluded_genre_names(self):
        """ Vérifie si les genres à exclure passé en paramètre existent dans 
            la base de donnée tellico"""
        if not excluded_genres: return
        allowed_string=self.xml_collection.find("tc:fields/tc:field[@name='genre']",ns).attrib["allowed"]
        alloweds=allowed_string.split(";")
        for genre in excluded_genres:
            if not genre in alloweds:
                raise ValueError("Le genre '"+genre+"' n'est pas valide. Possibilités: ["+allowed_string+"]")         
        
    
    def _init_items(self):
        """ Récupère les items (fiches ou cotes) qu'on doit imprimer """
        # ne garde que les livres dont il faut imprimer l'item (fiche ou cote).
        ## NOTE: la méthode findall("XPath") ne supporte pas notre filtre "entry_predicate",
        ## donc on fait ce filtrage à la main en parcourant tous les livres.
        xml_entries = self.xml_collection.findall('tc:entry',ns)          
        items = []
        for xml_entry in xml_entries:
            item = Item(xml_entry,self.item_type)
            if item.shall_be_printed: items.append(item)
        return items
    
    def __init__(self,item_type):
        # item_type -- fiches ou cotes        
        self.item_type = item_type
        # tellico_xml -- Le fichier xml de la base de donnée tellico
        self.tellico_xml=self._init_tellico_xml()
        # xml_collection -- Le noeud qui correspond à la collection de livre dans le fichier
        self.xml_collection=self.tellico_xml.getroot().find('tc:collection',ns)
        # valide les noms des genres à exclure (donnés en paramètre par l'utilisateur)
        self._validate_excluded_genre_names()
        # items -- La liste des fiches ou des cotes à imprimer
        self.items=self._init_items()
        # Le nombre total d'item à imprimer (on compte les copies multiples)
        self.print_count=sum(map(lambda item: item.print_count,self.items))
        # entry_predicate -- Le prédicat XPath qui permet de filtrer la liste des livres à imprimer:
        ## NOTE: entry_predicate doit être en accord avec la logique qui permet
        ## d'initialiser item.shall_be_printed de la classe Item       
            ## le nombre de fiche/de cote à imprimer doit être positif
        conditions=['./tc:'+print_count_db_name[item_type]+' > 0']
            ## la cote ne doit pas être vide
        conditions.append('boolean(./tc:cote)')
            ## le genre ne doit pas être exclu de l'impression
        if excluded_genres:
            condition = " and ".join("./tc:genre != '%s'"%genre for genre in excluded_genres)
            conditions.append(condition)
        self.entry_predicate = '['+" and ".join(conditions)+']'
        # DEPRECATED: Si tellico est lancé on récupère la liste des ids des livres filtrés:
        # Si il y a un filtre, on imprimera les fiches uniquement pour les éléments filtrés
        # joined_ids = ""
        # if tellico_is_launched:
            # dbus_tellico = bus.get_object("org.kde.tellico", "/Tellico")
            # ids = dbus_tellico.filteredEntries()
            # joined_ids = " or ".join("@id="+str(id) for id in ids)
            # entry_predicate+= "["+joined_ids+"]"
                # print_dir -- Le sous répertoire de "impressions" où seront stockées les impressions
                # des fiches (impressions/fiches) ou les cotes (impressions/cotes)
        self.print_dir = os.path.expanduser(output_dir+'/'+item_type)
        logging.info("--------------------")
        logging.info("Total:%i %s à imprimer",self.print_count,item_type)
        
    
    def clear_tellico_print_counts(self):
        """ Mets à jour tellico en fonction du pdf qui a été imprimé:
            Remet le nombre de cote ou de fiche à imprimer à zéro
        """          
        # Met à jour tellico pour chacun des items imprimés.
        for item in self.items: item.clear_print_count()

    def unlock_tellico_db(self):
        """ supprime le fichier xml temporaire, signalant ainsi que l'éventuelle
        mise à jour des données tellico est terminée.
        """
        shell_command(["rm",tmp_xml_path],check=False)
        # Affiche le temps écoulé pendant le blocage des mises à jour
        self.end = time.time()
        elapsed = self.end-self.start
        logging.debug("unlocked tellico db after %d seconds" % elapsed)
        
        
    def commit_tellico_xml(self):
        """ Mets à jour la base de donnée xml de tellico avec no modification
        """
        with open(tmp_xml_path, 'wb') as f:
            f.write(bytes(
                '<?xml version="1.0" encoding="UTF-8" ?>\n'+
                "<!DOCTYPE tellico PUBLIC '-//Robby Stephenson/DTD Tellico V11.0//EN' 'http://periapsis.org/tellico/dtd/v11/tellico.dtd'>\n",
                'utf-8'))
            self.tellico_xml.write(f,'utf-8')
        # Copie le fichier xml temporaire dans la base de données tellico
        shell_command(["zip","-r","-j",tellico_file_path,tmp_xml_path])        
        logging.info("Le fichier de sauvegarde de tellico a été mis à jour avec les données d'impression")


    def make_pdf(self):
        """ Génère le pdf à imprimer et l'ouvre, puis met à jour tellico """       
        # Si il n'y a rien à imprimer    
        if len(self.items)==0:
            # Supprime le fichier xml temporaire pour libérer l'accès à la base de donnée tellico
            self.unlock_tellico_db()
            logging.info("Rien à imprimer, fin du process")
            
            # affiche un message d'info
            message_text=("Il n'y a pas de "+self.item_type[:-1]+" à imprimer pour le moment.\n"
                         "Retrouvez les impressions déjà faites dans le répertoire 'impressions'")
            shell_command(['zenity','--info','--text=%s'%message_text])                        
            
            # ouvre le répertoire ou se trouvent archivées les impressions  
            open_path(self.print_dir)
                        
            return
        
        # Génère le fichier xml qui précise le mot clé correspondant à une
        # cote numérique
        self._init_docu_codes()
       
        # génère les fiches au format html en appliquant le template xsl
        # au fichier xml de la liste des livres.
        with open('/tmp/calandreta_'+self.item_type+'.html','w') as f:
            args=[  'xsltproc',
                    '--novalid',
                    '--param','entry_predicate','"'+self.entry_predicate+'"',
                    '--param','sort-name1',"'%s'"%sort[self.item_type],
                    input_dir+'/'+self.item_type+'.xsl',
                    tmp_xml_path    ]
            logging.debug(" ".join(args))
            subprocess.check_call(args,stdout=f)

        # copie le fichier de mise en forme CSS
        shell_command(['cp',input_dir+'/'+self.item_type+'.css','/tmp/'+self.item_type+'.css'])

        # utilise le fichier html pour générer un pdf prêt à imprimer 
        if not os.path.exists(self.print_dir): os.makedirs(self.print_dir)
        output_file_path = self.print_dir+'/'+datetime.now().strftime("%Y_%m_%d-%Hh%M")+'.pdf'
        args=['wkhtmltopdf']
        args.extend(wk_options[self.item_type])
        args.append('/tmp/calandreta_'+self.item_type+'.html')
        args.append(output_file_path)
        shell_command(args)
                
        # ouvre le pdf pour que l'utilisateur le voie et puisse l'imprimer
        logging.info("Impression faites dans %s",output_file_path)
        open_path(output_file_path)
        
        # remet les compteurs d'impression à zéro
        self.clear_tellico_print_counts()
        
        # Si tellico n'est pas lancé il faut enregistrer les modifications dans la base de données xml
        if not tellico_is_launched:self.commit_tellico_xml()        
        
        # Supprime le fichier xml temporaire pour libérer l'accès à la base de donnée tellico
        self.unlock_tellico_db()


# génère le pdf et met à jour tellico
try:
    PrintManager(args.item_type).make_pdf()
except Exception as e:
    # Si une erreur survient:
    # supprime le fichier temporaire qui vérouille l'accès à la base de données
    # Tellico
    shell_command(["rm",tmp_xml_path],check=False)
    raise e
    
    


