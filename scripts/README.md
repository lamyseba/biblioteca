---
auteur: Sébastien Lamy (lamyseba arobase free.fr)
---

Utilisation des scripts
===========================================================

Le répertoire `scripts` contient des scripts pour faciliter la gestion d'une 
petite bibliothèque d'école qui utilise le programme [Tellico][] pour le 
catalogage des livres.

[Tellico]:http://tellico-project.org/



impression.py
-------------------------------------
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

### Syntaxe
```bash
impression.py [-h] [--log LOG] [--genre GENRE] [--eco] [-s SORT] item_type

Le premier argument indique s`il faut imprimer les fiches ou les cotes : Ce 
script ne fait pas les deux à la fois.

positional arguments:
  item_type          peut prendre la valeur "fiches" ou "cotes"

optional arguments:
  -h, --help            show this help message and exit
  --log LOG             info or debug
  --genre GENRE         la liste des genres à traiter, séparés par des ';'. 
                        Si la liste commence par un '!', les genres donnés 
                        seront exclus et les autres seront traités
  --eco                 pour les fiches: n`imprime que les pages pleines
  -s SORT, --sort SORT  le tri souhaité pour l`impression, séparés par des ';'. 
                        Par défaut 'cote' pour les cotes et 'ID' pour les fiches
```

### Exemples d'utilisation
En supposant que vous soyez placé dans le répertoire racine du projet.
```bash
# Imprime toutes les fiches manquantes
./scripts/impression.py fiches 

# Imprime les cotes manquantes de tous les livres qui ne sont pas du 
# genre "Documentaire" ni du genre "Album"
./scripts/impression.py cotes --genre \!"Documentaire;Album" 

# Imprime les cotes manquantes de tous les livres qui sont du genre 
# "Documentaire" ou du genre "Album"
./scripts/impression.py cotes --genre "Documentaire;Album"

# Imprime toutes les fiches manquantes et détaille le déroulé sur la sortie 
# standard (au lieu de l'écrire dans le fichier de log)
./scripts/impression.py fiches --log debug

# Imprime toutes les fiches manquantes pour les livres qui ne sont pas du
# genre "Documentaire" et n'imprime que les pages pleines
./scripts/impression.py fiches --genre \!Documentaire --eco

# Imprime toutes les fiches manquantes pour les livres du genre 'Documentaire'
# et tri par cote puis par ID si la cote est la même:
./scripts/impression.py fiches --genre Documentaire --sort cote;ID
```



---
web.sh
-------------------------------------
Génère une page internet montrant les livres du catalogue, puis la met 
en ligne sur le site de l'école. La page inclut un champs de recherche. On 
peut cliquer sur une colonne pour trier suivant cette colonne.

Ce script ne prend pas d'option, il peut être lancé depuis la ligne de commande.
On peut aussi utiliser [anacron] pour le lancer automatiquement tous les jours.

### Exemple d'utilisation
En supposant que vous soyez placé dans le répertoire racine du projet.
```
./scripts/web.sh
```



---
github_push.sh
-------------------------------------
Sauvegarde le catalogue `inventaire.tc`, ainsi que le répertoire `docs` 
(cette documentation). Cette sauvegarde est effectué par un commit
suivi d'un push sur le site [github](https://github.com/lamyseba/biblioteca/)

Ce script ne prend pas d'option, il peut être lancé depuis la ligne de commande.
On peut aussi utiliser [anacron] pour le lancer automatiquement tous les jours.

### Exemple d'utilisation
En supposant que vous soyez placé dans le répertoire racine du projet.
```
./scripts/github_push.sh
```

[anacron]:http://www.delafond.org/traducmanfr/man/man8/anacron.8.html



---
rename_authors.py
-------------------------------------
Ce programme permet de changer le format des noms d'auteurs. On est parti sur un 
format "Dupont, Jean" pour l'inventaire, mais on se réserve la possibilité 
d'adopter  "Jean Dupont" à l'avenir, même si [une réflexion][] nous indique 
c'est peu probable. Ce script peut être lancé en ligne de commande depuis un 
terminal.

### Syntaxe

```bash
rename_authors.py [-h] [-v] input_file output_file

positional arguments:
  input_file     le fichier de base de donnée tellico à transformer
  output_file    le nom du fichier de sortie (par defaut:output.tc)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  affiche les transformations de nom sur la sortie standard
```

### Exemples d'utilisation
En supposant que vous soyez placé dans le répertoire racine du projet.
```bash
# Renomme les auteurs du fichier inventaire.tc au format 'Prénom' 'Nom' et 
# enregistre le résultat dans le fichier inventaire_new.tc
./rename_authors.py inventaire.tc inventaire_new.tc

# Renomme les auteurs en modifiant directement le fichier inventaire.tc et
# en affichant les transformation de nom dans la console:
./rename_authors.py -v inventaire.tc inventaire.tc
```

[une réflexion]:https://lamyseba.github.io/biblioteca/format-noms-d-auteur.html



---
doc.py
-------------------------------------
Génère la documentation du projet (celle que vous consultez maintenant): 
interprète les fichiers au format Markdown du répertoire `docs/sources` pour 
générer les fichiers html dans le répertoire `docs`.

* Les fichiers au format Markdown sont consultables et modifiables avec un 
  éditeur de texte simple (notepad, gedit). Leur nom se termine par l'extension
  `.md`
* Les fichiers html sont des fichiers lus par les navigateurs web (firefox,
  chrome...). La documentation du projet se trouve au format html dans le
  répertoire `docs`.

Ce script peut être lancé en ligne de commande depuis un terminal, mais on 
peut aussi cliquer sur le lanceur `Générer html` dans le dossier `docs/sources`
pour exécuter ce script sans option.

Avec l'option -i, ce script ne génère pas la documentation mais met à jour
l'icone du lanceur `Documentation` à la racine du projet.  

Pour plus d'information sur la consultation et la modification de la 
documentation, consultez [la page dédiée](utiliser-la-documentation.html)


### Syntaxe
```bash
doc.py [-h] [-i]

optional arguments:
  -h, --help  show this help message and exit
  -i, --icon  Mets à jour l`icone du lanceur (au lieu de générer la
              documentation)
```

### Exemples d'utilisation
En supposant que vous soyez placé dans le répertoire racine du projet.
```bash
# Génère la documentation à partir de tous les fichier .md du répertoire
# docs/src
./scripts/doc.py

# Met à jour l'icone du lanceur `Documentation`, à la racine du projet
./scripts/doc.py -i
```


___

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
* Un interpréteur python, ainsi que les librairies `python-dbus` et `python-markdown`



_(1) Pour la petite histoire, cette version est compilée avec une version 
patchée de Qt, et souvent la version disponible dans le dépot de votre distro
linux favorite n'est pas compilée avec cette version patchée_


[wkhtmltopdf]:https://wkhtmltopdf.org/
