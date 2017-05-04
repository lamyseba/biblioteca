# biblioteca

Des scripts pour faciliter la gestion d'une petite bibliothèque d'école qui 
utilise le programme [Tellico][] pour le catalogage des livres.



### Fonctionnement de la bibliothèque d'école Calandreta Pau:
Les livres sont catalogués sur Tellico. Une [page internet générée à partir
du catalogue][] est disponible en ligne.

La gestion des emprunts de livre ne se fait pas informatiquement, mais grâce
à des fiches. Un livre est prêté à une classe (ex: la classe de CP), pas à 
un élève en particulier. Dans la bibliothèque il y a donc une boite pour
chacune des cinq classes de l'école. Dans la boite d'une classe se trouvent 
les fiches de tous les livres empruntés par les élèves de cette classe.

Cette organisation n'a pas été choisie faute de moyen informatiques pour
gérer les emprunts, mais pour permettre un fonctionnement courant de la 
bibliothèque avec très peu de moyen humain. Voir les [questions/réponses]
sur ce sujet.



### A quoi servent ces scripts?
Les scripts de ce projet sont dans le répertoire [CodeSource][]
et répondent aux besoins suivant:

* [impression.py][]
    * Imprimer des fiches pour les livres qui en ont besoin
    * Imprimer des cotes pour les livres qui en ont besoin
* [web.sh][]: Générer une page internet qui présente les livres du catalogue et 
  mettre cette page en ligne. Cette page inclus un champs de recherche. On peut 
  cliquer sur une colonne pour trier suivant cette colonne.
* [gitbackup.sh][]: Sauvegarder le catalogue sur github (eh oui ici même!)
* [rename_authors.py]: Changer le format des noms d'auteurs. On est parti sur
  un format "Dupont, Jean", mais on se réserve la possibilité d'adopter
  "Jean Dupont" à l'avenir.



### Qui utilise ces scripts?
Les personnes qui s'occupent de la bibliothèque ne sont pas toutes des fanas
de la ligne de commande. Ces personnes gèrent l'impression des fiches et des
cotes simplement en double-cliquant sur les raccourcis `impression_fiches` et
`impression_cotes` à la racine du projet. Ces raccourcis lancent le script 
`impression.py` avec les paramètres qui vont bien

Pour des besoins plus particuliers, un utilisateur aguerri peut utiliser 
`impressions.py` directement en ligne de commande.

Chez nous, les scripts `web.sh` et `gitbackup.sh` sont lancés automatiquement au 
chaque jour au démarrage de l'ordinateur de la bibliothèque (grâce à [anacron][])



### Il y a des dépendances à installer?
C'est mieux de partir avec Tellico, bien sur! Ces scripts s'appuient sur un 
catalogue Tellico customisé avec des champs supplémentaires, notamment pour 
gérer le nombre d'impression de fiche ou de cote pour chaque livre. 
Le catalogue `inventaire.tc` (à la racine du projet) fonctionne bien avec
les scripts: c'est le catalogue à jour de notre école! Vous pouvez l'ouvrir avec
Tellico, puis le vider pour le re-remplir avec vos propres références.

Les scripts utilisent des programmes en ligne de commande, qui doivent être 
installés sur l'ordinateur:
 
* [xsltproc] : utilisé pour générer une page html à partir des données du 
  catalogue
* [wkhtmltopdf] : utilisé pour transformer la page html en pdf à imprimer  
  _**Note:** La version disponible par défaut dans les dépôts de la plupart des 
  distrib donne une mauvaise sortie pdf car elle ignore l'option 
  `--disable-smart-shrinking` fournie par le script. Si cela vous arrive, 
  téléchargez la version fournie sur le site en ligne(1). Placez ensuite 
  l'executable dans /usr/bin. Par ex:_
  
        sudo cp ~/Téléchargement/dossier_wkhtml_dezipé/bin/wkhtmltopdf /usr/bin
    
* la commande ftp doit être disponible (c'est le cas la plupart du temps)
* Un interpréteur python, et la librairie DBUS pour python (python-dbus)


Pour plus de renseignement sur le fonctionnement de la bibliothèque de l'école,
vous pouvez consulter le wiki.

_(1) Pour la petite histoire, cette version est compilée avec une version 
patchée de Qt, et souvent la version disponible dans le dépot de votre distro
linux favorite n'est pas compilée avec cette version patchée_


[Tellico]:http://tellico-project.org/
[CodeSource]:tree/master/CodeSource
[impression.py]:blob/master/CodeSource/web.sh
[web.sh]:blob/master/CodeSource/web.sh
[gitbackup.sh]:blob/master/CodeSource/gitbackup.sh
[rename_authors.py]:blob/master/CodeSource/rename_authors.py
  
___

## Questions/Réponses
### Pourquoi Tellico pour le catalogage?


### Les données bibliographiques sont-elles récupérées en ligne?
Les fonctions de récupération des
données bibliographiques sur des serveurs ne sont pas utilisées pour le moment,
même si Tellico permet notamment de récupérer ce type de données sur les 
serveur de la BNF.

### Pourquoi une gestion des prêts par fiches?

___

## Traitement des acquisitions de la bibliothèque

Les nouveaux livres qui sont acquis par la bibliothèque suivent le processus
suivant

1. Nettoyage
2. Réparation si nécessaire
3. Couverture
4. Ajout d'un bandeau horizontal de couleur en haut du dos si le livre n'est pas 
  en français  
    * rouge: occitan
    * jaune: langue étrangère
  Si le livre est bilingue français/occitan ou français/étranger, on barre
  le bandeau de couleur d'un trait blanc horizontal/
  _NDLR: eh oui nous sommes une école occitane, donc beaucoup de livres avec un 
  bandeau rouge_
5. Ajout d'un support en carton en fin de livre, qui permet de fixer la fiche

