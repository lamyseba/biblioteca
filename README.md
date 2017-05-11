Ce document traite de la gestion de la bibliothèque de l'école. La documentation des 
scripts, qui participent à cette gestion, se trouve dans le [README][] du répertoire 
`CodeSource` du projet

___

## Questions / Réponses



### Pourquoi Tellico pour le catalogage?
Le logiciel utilisé pour le catalogage devait répondre au cahier des charges
suivant:

* __Disponible hors-ligne__ :
  * L'ordinateur de la bibliothèque n'était pas connecté à internet ni 
  * au réseau local au début du projet
  * Nous ne souhaitons pas dépendre d'une connexion réseau disponible pour le
    catalogage.
  * Nous sommes frileux pour confier l'hébergement de nos données à un tiers.
    Il faut en tout cas pouvoir les exporter facilement vers un nouveau
    logiciel si besoin. Tellico permet l'export dans de nombreux formats,
    dont le csv, qui est très répandu.
* __Prise en main facile__ pour les enseignants, les bénévoles, et les élèves
* __Gestion des doublons__ : Lors du catalogage, nous voulions détecter
  le nombre d'exemplaire de chaque livre. Le logiciel choisi devait nous aider
  dans cette tâche. L'auto-complétion avec liste de suggestion, disponible dans 
  Tellico nous assiste efficacement dans cette tâche
* __OpenSource__ : Le partage des connaissances, la liberté et la curiosité 
  font partie de nos valeur.

Dans un premier temps, nous avons commencé à utiliser une simple feuille
`libreoffice calc`. Puis nous avons migré vers Tellico pour la simplicité
et la convivialité de son interface.



### Les données bibliographiques sont-elles récupérées en ligne?

Tellico permet la récupération des données bibliographiques sur des serveurs, 
comme par exemple le serveur de la BNF. Nous n'utilisons pas cette 
fonctionnalité pour le moment.

Dans notre cas en effet, le nombre de données à saisir pour chaque livre est
relativement peu important (Titre, Auteur, Éditeur, Langue). Nos données de 
catalogage comprennent aussi des informations qui ne sont pas disponibles sur
le serveur BNF: code de rangement interne, statut de l'impression des fiches,
nombre d'exemplaires dans notre stock.
Enfin, nous n'utilisons pas tout à fait les mêmes conventions de saisie que
le serveur BNF:
* Le serveur de la BNF ne met pas l'illustrateur dans la liste des auteurs, mais 
  dans les commentaires, ce qui ne correspond pas à notre logique (nous voulons 
  pouvoir regrouper les livres par illustrateur aussi).
* Le serveur BNF ne sépare pas le nom et le prénom de l'auteur par une virgule,
  mais par un espace, ce qui ne permet pas de les distinguer.

Au total, il aurait fallu systématiquement remodifier les données importées du
serveur, le gain de temps nous semble incertain. Il est cependant possible que
nous utilisions à l'avenir cette fonctionnalité de Tellico pour compléter nos
données bibliographique.




### Pourquoi une gestion des prêts par fiches?
21è siècle, l'ère du code-barre. Et pourtant!

Loin du modèle de bibliothèque classique avec un ou plusieurs employés pour
gérer le stock, les prêts et le rangement des livres, notre bibliothèque repose
sur le bénévolat quand il est disponible, les enseignants et les élèves le reste
du temps. La ou les personnes qui viennent emprunter des livres ont de grandes
chances de se trouver seule(s) dans la bibliothèque.

Dans ce contexte, demander aux élèves ou aux enseignants d'allumer l'ordinateur,
de lancer le programme, d'identifier la classe et de scanner les codes barres
nécessaires relève presque de l'utopie.
La logique "Mets la fiche dans la boite de ta classe avant d'emporter le livre"
nous a semblé plus accessible pour les enseignants et surtout les élèves.
Bien sur il y aura des ratés, des fiches pas rangées, mais l'objectif au 
sein de l'école est d'avoir un système de prêt qui permet le plus de souplesse
possible dans la pratique, plutôt qu'un système _théoriquement_ très rigoureux.

