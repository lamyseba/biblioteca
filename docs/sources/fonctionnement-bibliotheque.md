---
auteur: Sébastien Lamy (lamyseba arobase free.fr)
---

Fonctionnement de la bibliothèque d'école Calandreta Pau
===========================================================

La bibliothèque fonctionne avec très peu de moyen humain. Des bénévoles assurent
le traitement des acquisitions des livres, ainsi qu'un peu de rangement. Les 
utilisateurs de la bibliothèque (élèves et enseignant) doivent pouvoir la faire
vivre quasiment en autonomie (donc gérer les emprunts et le rangement).



Inventaire des livres
-------------------------------------
L'inventaire est stocké dans le fichier `inventaire.tc` à la racine du projet.
Les données y sont stockées au format XML, puis compressées avec ZIP.
C'est un fichier exploitable par le programme Tellico.


### Consultation de l'inventaire
Le programme [Tellico][], disponible sur l'ordinateur de la bibliothèque de 
l'école, permet de consulter l'inventaire et d'y faire des recherches. On peut 
le lancer depuis le bureau de l'ordinateur, ou bien par un double clic sur le 
fichier `inventaire.tc`.

Le catalogue peut aussi être consulté en ligne sur le site internet de l'école,
à l'adresse <http://calandreta-pau.org/bibli/>. C'est le script [web.sh][] qui 
génère la page internet à partir du fichier `inventaire.tc`


### Ajout d'un livre à l'inventaire
Pour ajouter un livre à l'inventaire, il faut saisir manuellement les données
qui le concernent dans le programme Tellico. Notre école a choisi une 
[norme pour la saisie des données][], n'oubliez pas de la consulter!!! Cette
norme de saisie impacte notamment le formattage des cotes imprimées.

Lors de l'enregistrement du livre dans l'inventaire, les données suivantes sont
automatiquement rajoutées pour le livre:

* **N°** : Le numéro d'inventaire du livre
* **Créé le** : La date à laquelle le livre a été ajouté à l'inventaire.

!!! important ""
    **Pensez à écrire le numéro d'inventaire sur la page de titre du livre !!**
    Ce numéro est diponible une fois le livre enregistré dans l'inventaire. Il 
    se trouve dans la colonne `N°` de la ligne qui correspond au livre.

La fonction de récupération en ligne de données bibliographique n'est pas 
utilisée pour le moment. Voir les [Questions/Réponses sur ce sujet](questions-reponses.html#les-données-bibliographiques-sont-elles-récupérées-en-ligne)



### Sauvegarde de l'inventaire
Le script [github_push.sh][] permet de sauvegarder le fichier `inventaire.tc`
sur github. [Anacron][] lance ce script tous les jours où quelqu'un allume 
l'ordinateur




Gestion des emprunts
-------------------------------------
La gestion des emprunts de livre ne se fait pas informatiquement, mais **grâce
à des fiches**. La fonction de gestion des emprunts de Tellico n'est pas utilisée. 

Nous considérons qu'un livre est prêté à une classe (ex: la classe de CP), pas à 
un élève en particulier. Dans la bibliothèque il y a donc une boite pour
chacune des cinq classes de l'école. 

![cinq boites](images/boites.png)

Dans la boite d'une classe se trouvent les fiches de tous les livres empruntés 
par les élèves de cette classe.

Cette organisation n'a pas été choisie faute de moyen informatiques pour
gérer les emprunts, mais pour permettre un fonctionnement courant de la 
bibliothèque avec très peu de moyen humain. Voir les 
[Questions/Réponses sur ce sujet](questions-reponses.html#pourquoi-une-gestion-des-prêts-par-fiches).





Traitement des acquisitions de la bibliothèque
-------------------------------------
Les nouveaux livres qui sont acquis par la bibliothèque suivent le processus
suivant.

1. Nettoyage.
2. Réparation si nécessaire.
3. Couverture.
4. Ajout d'un bandeau horizontal de couleur en haut du dos si le livre n'est pas 
  en français  
    * occitan: rouge.
    * langue étrangère : jaune.
    * bilingue français/occitan ou français/étranger :  le bandeau est rouge ou 
      jaune selon la langue, mais il est barré d'un trait blanc sur toute sa
      longueur.
5. Ajout d'une pochette en fin de livre, qui permet de glisser la fiche.
6. Inventorier le livre utilisant le programme Tellico. Dans notre école, il y a 
   une [norme pour la saisie des données][]. N'oubliez pas de la consulter!   
   <div class="admonition important">Une fois que le livre est enregistré dans 
   l'inventaire, il faut **recopier le N° d'inventaire sur la page de titre du 
   livre**.</div>
7. Impression et mise en place de la fiche. L'impression se fait grâce au 
   raccourci `Impression des fiches` à la racine du projet. Un double-clic
   sur ce raccourci lance le script [impression.py][] avec le paramétrage 
   nécessaire. 
8. Impression et mise en place de la cote. L'impression se fait grâce au
   raccourci `Impression des cotes` à la racine du projet. Un double-clic
   sur ce raccourci lance le script [impression.py][] avec le
   paramétrage nécessaire.
9. Rangement dans le rayon adéquat.

Pour chaque étape, un emplacement est réservé dans le rayonnage. On y trouve
tous les livres qui n'ont pas encore passé cette étape. Après avoir traité
le livre, on le range dans le rayon de l'étape suivante à effectuer pour
ce livre.
 
* [ ] TODO: rédiger un document spécifique à l'impression des fiches : où se
  trouve le pdf, comment paramétrer l'imprimante, que faire si des fiches sont
  mal imprimées, etc...
* [ ] TODO: intégrer une vidéo de démonstration: "Comment couvrir".



[Tellico]:http://tellico-project.org/
[impression.py]:utilisation-des-scripts.html#impressionpy
[web.sh]:utilisation-des-scripts.html#websh
[github_push.sh]:utilisation-des-scripts.html#github_pushsh
[rename_authors.py]:utilisation-des-scripts.html#rename_authorspy
[anacron]:http://www.delafond.org/traducmanfr/man/man8/anacron.8.html
[page internet générée à partir du catalogue]:http://calandreta-pau.org/bibli/
[Ajout d'un livre à l'inventaire]:#ajout-dun-livre-à-linventaire
[norme pour la saisie des données]:norme-saisie-livre.html

