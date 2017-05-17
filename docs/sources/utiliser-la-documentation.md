---
auteur: Sébastien Lamy (lamyseba arobase free.fr)
---

Utiliser la documentation
===========================================================

A quoi sert la documentation ?
-------------------------------------
La documention permet de comprendre le fonctionnement courant de la bibliothèque
calandreta paulina. Elle parle aussi des réflexions et des choix qui ont 
aboutis à ce fonctionnement. Enfin, elle sert de manuel informatique et
technique pour la maintenance de la bibliothèque.


Naviguer
-------------------------------------
Le **sommaire de la documentation** est accessible depuis toutes les pages de la
documentation, en cliquant sur le **titre principal en haut de page** (ce titre
se nomme "Documentation", comme par hasard).


Le format Markdown
-------------------------------------
La documentation est écrite au format _Markdown_. C'est une façon simple d'écrire 
un texte avec des titres, des liens, des passages en gras ou en italique.
Un fichier _Markdown_ s'écrit et se modifie avec **un éditeur de texte simple** 
(notepad sous Windows par exemple, ou gedit sous Ubuntu).

Le mieux pour l'apprendre est de [pratiquer un peu][] en pouvant consulter [un mémo][].
[pratiquer un peu]:http://markdown.pioul.fr/
[un mémo]:memo-markdown.html


Modifier une page
-------------------------------------
En bas de chaque page de documentation, un lien pointe vers le **fichier source**
de la page. C'est ce fichier qu'il faut modifier pour modifier la page. Les 
fichiers sources de la documentation sont écrits au format Markdown.
Cliquez sur le lien puis sur `ouvrir` (et non pas sur `Télécharger`). Ou bien
retrouvez le fichier dans le répertoire `docs/sources` du projet.

Une fois le fichier modifié et enregistré, il faut 
[générer la documentation](#générer-la-documentation-à-partir-des-sources).
N'oubliez pas de rafraîchir la page de votre navigateur pour voir le résultat
(par exemple en appuyant sur la touche `F5` de votre clavier)


Ajouter une page
-------------------------------------
Le dossier `docs/sources` est l'endroit où se trouvent les fichiers sources de
la documentation. Pour ajouter une page à la documentation, il faut ajouter un 
fichier texte à ce dossier: Écrivez votre texte au format Markdown dans un 
éditeur de texte simple et enregistrez le fichier dans ce dossier.
Evitez les _espaces_ et les caractères autre que _lettre sans accent_, _tiret -_,
*tiret _* dans le nom du fichier, et terminez ce nom par `.md` pour 
signifier qu'il s'agit d'un fichier Markdown. Exemple: `mon-nom-de-fichier.md`

Ensuite, il peut être interessant de modifier le sommaire de la documentation,
pour ajouter un lien vers votre nouvelle page, avec une brève description. Si 
vous avez bien lu cette page vous savez déjà comment modifier le sommaire. 
Le lien vers votre page depuis le sommaire est : `mon-nom-de-fichier.html`, **sans**
_http://_, ni rien d'autre devant ou derrière. En effet le sommaire et votre
nouvelle page sont dans le même répertoire, donc nul besoin d'aller chercher sur
internet ou dans un autre répertoire.

Une fois que tout ça est fait, il ne vous reste plus qu'à générer la 
documentation, et à la consulter dans votre navigateur (il faudra peut-être 
rafraichir la page du sommaire, par un appui sur la touche `F5`)


Générer la documentation à partir des sources
-------------------------------------
C'est le script `doc.py` qui se charge de ce travail. Ceux qui aiment parler à 
leur ordinateur en lui écrivant poliment des mots peuvent ouvrir une console 
(`CTRL+ALT+T` sous Ubuntu), puis lui demander de se déplacer dans le dossier
`scripts` du projet. Par exemple:

    cd Bibli/scripts

Puis lui demander d'exécuter le script:

    ./doc.py

Ceux qui préfèrent ne pas adresser la parole à leur machine mais plutôt lui
faire des gestes ne se rendront pas au même endroit: ils cliqueront jusqu'à ce
que leur ordinateur veuille bien leur montrer le contenu du dossier `docs/sources` 
du projet. Là, ils trouveront entre autre le lanceur `Générer html`. Un double 
clic sur ce lanceur signifiera pour votre ordinateur: 
"Eh! Toi, là! Réveille-toi et génère-moi la documentation! Tu vois bien que
j'attends!".
