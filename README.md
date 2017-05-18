
biblioteca
===========================================================
Ce projet a été conçu pour répondre aux besoins de notre petite bibliothèque
d'école: 
* Inventorier des livres;
* Présenter une version en ligne de l'inventaire;
* Imprimer des fiches et des cotes pour les livres;
* Faire une copie de sauvegarde de l'inventaire sur github

Avant d'utiliser ce projet, assurez vous que vous avez des besoins similaires...
Vous pouvez consulter le fonctionnement détaillé de notre bibliothèque dans 
[la documentation][1]. Vous y trouverez notamment [les raisons][] qui nous ont fait 
choisir une gestion des prêts par fiche.

[les raisons]:http://lamyseba/github.io/bilioteca/questions-reponses.html#pourquoi-une-gestion-des-prêts-par-fiches




Installation
-------------------------------------
Clonez ce projet dans le répertoire de votre choix. Pour que les scripts 
fonctionnent, il faudra peut être installer des dépendances (voir 
[le README du dossier des scripts][2])



Utilisation
-------------------------------------
Assurez-vous que le programme [Tellico][] est bien installé sur votre ordinateur,
puis ouvrez le fichier `inventaire.tc` (c'est un fichier de catalogue pour Tellico).
Supprimez toutes les livres enregistrés, et remplacez par vos propres livres.

Par contre, gardez bien les champs définis dans ce catalogue. Certains champs
spéciaux sont utilisés pour décompter les impressions de fiches et de cotes
qu'il reste à faire.

Logiquement, la réponse à vos autres question devrait se trouver dans 
[la documentation][1].



Documentation
-------------------------------------
[La documentation][1] est en ligne sur github-pages, vous pouvez aussi la
retrouver directement dans le répertoire `docs` du projet.
Commencer par le fichier `index.html` peut être une bonne idée.


[1]:https://lamyseba.github.io/biblioteca/
[2]:scripts/README.md#il-y-a-des-dépendances-à-installer
[Tellico]:http://tellico-project.org/