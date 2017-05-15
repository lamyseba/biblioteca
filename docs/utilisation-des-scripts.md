---
auteur: Sébastien Lamy (lamyseba arobase free.fr)
---

Utilisation des scripts
===========================================================

Le répertoire `scripts` contient des scripts pour faciliter la gestion d'une 
petite bibliothèque d'école qui utilise le programme [Tellico][] pour le 
catalogage des livres.

[Tellico]:http://tellico-project.org/



### impression.py
Un automate pour imprimer les fiches et les cotes pour les livres qui en ont
besoin. Ce programme génère un pdf et met à jour le fichier d'inventaire: il
remet à zéro le nombre de fiche ou de cote à imprimer pour les livres concernés.

```bash
# > ./impression.py -h
usage: impression.py [-h] [--log LOG] [--exclude EXCLUDE] item_type

positional arguments:
  item_type          peut prendre la valeur "fiches" ou "cotes"

optional arguments:
  -h, --help         show this help message and exit
  --log LOG          info or debug
  --exclude EXCLUDE  la liste des genres à exclure, séparés par des ';'
```


### web.sh
Ce script génére une page internet montrant les livres du catalogue, puis la met 
en ligne sur le site de l'école. Cette page inclut un champs de recherche. On 
peut cliquer sur une colonne pour trier suivant cette colonne.



### github_backup.sh 
Ce script sauvegarder le catalogue `inventaire.tc` sur github



### rename_authors.py
Ce programme permet de changer le format des noms d'auteurs. On est parti sur un 
format "Dupont, Jean" pour l'inventaire, mais on se réserve la possibilité 
d'adopter  "Jean Dupont" à l'avenir, même si [une réflexion][] nous indique 
c'est peu probable.

```bash
# > ./rename_authors.py -h
usage: rename_authors.py [-h] [-v] input_file output_file

Ce script permet de renommer tous les auteurs de la base Tellico: Tous les
auteurs saisis sous la forme "Dupont, Jean" deviendront: "Jean Dupont".

positional arguments:
  input_file     le fichier de base de donnée tellico à transformer
  output_file    le nom du fichier de sortie

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  affiche les transformations de nom sur la sortie standard

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
```

[une réflexion]:../docs/format-noms-d-auteur.md



___

Qui utilise ces scripts?
-------------------------------------
Les personnes qui s'occupent de la bibliothèque ne sont pas toutes des fanas
de la ligne de commande. Ces personnes gèrent l'impression des fiches et des
cotes simplement en double-cliquant sur les raccourcis `impression_fiches` et
`impression_cotes` à la racine du projet. Ces raccourcis lancent le script 
`impression.py` avec les paramètres qui vont bien.

Pour des besoins plus particuliers, un utilisateur aguerri peut utiliser 
`impressions.py` directement en ligne de commande.

Chez nous, [anacron][] lance automatiquement les scripts `web.sh` et 
`github_backup.sh` chaque jour où l'ordinateur de la bibliothèque est allumé.

[anacron]:http://www.delafond.org/traducmanfr/man/man8/anacron.8.html




Il y a des dépendances à installer?
-------------------------------------
C'est mieux de partir avec Tellico, bien sur! Ces scripts s'appuient sur un 
catalogue Tellico customisé avec des champs supplémentaires, notamment pour 
gérer le nombre d'impression de fiche ou de cote pour chaque livre. 
Le catalogue `inventaire.tc` (à la racine du projet) fonctionne bien avec
les scripts: c'est l'inventaire à jour des livres de notre école! Vous pouvez 
l'ouvrir avec Tellico, puis le vider pour le re-remplir avec vos propres
références.

Les scripts utilisent des programmes en ligne de commande, qui doivent être 
installés sur l'ordinateur:
 
* `xsltproc` est utilisé pour générer une page html à partir des données du 
  catalogue. Ce programme fait partie du paquet `libxslt` installé dans 
  la plupart des distribution linux.
* [wkhtmltopdf][] : utilisé pour transformer la page html en pdf à imprimer  
  _**Note:** La version disponible par défaut dans les dépôts de la plupart des 
  distrib donne une mauvaise sortie pdf car elle ignore l'option 
  `--disable-smart-shrinking` fournie par le script. Si cela vous arrive, 
  téléchargez la version fournie sur le site en ligne(1). Placez ensuite 
  l'executable dans /usr/bin :_  
  ```bash  
    sudo cp ~/Téléchargement/dossier_wkhtml_dezipé/bin/wkhtmltopdf /usr/bin
  ```  
* la commande `ftp` doit être disponible (c'est le cas la plupart du temps)
* Un interpréteur python, et la librairie `python-dbus`



_(1) Pour la petite histoire, cette version est compilée avec une version 
patchée de Qt, et souvent la version disponible dans le dépot de votre distro
linux favorite n'est pas compilée avec cette version patchée_


[wkhtmltopdf]:https://wkhtmltopdf.org/
