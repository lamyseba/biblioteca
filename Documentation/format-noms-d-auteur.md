
RÉFLEXION SUR LE FORMAT DE SAISIE DES NOMS D'AUTEUR
=====================================



Complétion automatique du nom d'auteur lors de la saisie d'un nouveau livre
-------------------------------------
Problèmes:

 * Pour les auteurs ou le prénom n'est pas fourni sur certains livres, mais
   est disponible sur d'autres
 * Pour les auteurs dont seul l'initiale du prénom est fournie sur le livre
 * Pour les couples (deux prénoms et un seul nom)



Mise en forme automatique
-------------------------------------
Tellico propose la mise en forme automatique des noms : "Jean Dupont" peut
s'afficher "Dupont, Jean" si on coche l'option. Cette mise en forme 
automatique ne touche pas aux données réelles.).

Problèmes:

 * Affichage du nom de certains auteurs (voir cette liste)
 * Peut provoquer un comportement erroné de saisie, aussi bien en recherche
   qu'en ajout de donnée (on a tendance a chercher les noms comme il sont mis
   en forme, mais ce n'est pas ainsi qu'il sont stockés et accessibles en 
   réalité)



Noms d'auteurs qui peuvent poser problèmes
-------------------------------------
Ces noms ont été relevés dans le fichier de base de donnée de la bibliothèque 
Calandreta Pau

### Particules
La mise en forme automatique marche bien, mais laisse la particule en tête.

    De Sainte-Croix, Georges
    de Saint-Blanquat, Henri 
    D'Alençon, May
    Le Bloas, Renée
    El Khier,Oum 
    Del Hup, Henri
    De Boeck, Francine 
    Le Pavec, Marie-Claire
    Le Guillouzic, Noëlle
    dau Melhau, Jan->Jan dau Melhau
    Van Laan, Nancy

### Couples
La mise en forme automatique marche bien

    Escholier, Marie et Raymond 
    Guion, Jeanine et Jean
    Guion,  Jeanine et Jean->Jeanine et Jean Guion
    Grimm, Jacob et Wilhelm 

### Noms solidaires
La mise en forme automatique pose problème

    Total guide
    Pomme d'api
    La Chapelle Mémorial de l'Aviation
    Parc national des Pyrénées
    Parc National des pyrénées
    Leprince de Beaumont
    De Bélizal
    De Franciscis
    Le coz
    Feutre Fulda France

### Prénom composé sans tiret
La mise en forme automatique marche bien

    Alfaenger, Peter K.
    Dubois, Claude K.
    Stockton, Franck R.
    Versini, Roussel Anne
    Pararamon, Josep Maria
    Pertuzé, Joan Claudi
    Cauhapè, Maria Elena

### Noms composés sans tiret
La mise en forme automatique ne marche pas

    Solé Vendrell, Carme
    Peña Santiago, L.-P.
    Garcia Sanchez, J.L.
    Hong Chen, Jian

### Prénom et noms composés sans tiret
La mise en forme automatique **ne marche pas**

    Alibés i Riera, M. Dolors


### Divers
La mise en forme automatique marche bien

    Winship, F.S.->F.S. Winship
    Pacheco, M.A.->M.A. Pacheco
    Dumeaux, M.-O.->Dumeaux M.-O.
    Langelier, J.-Pierre->J.-Pierre Langelier



Conclusion
-------------------------------------
Garder la mise en forme actuelle (séaparé par une virgule). Le script
CodeSource/rename_authors.py permettra par la suite de migrer tous les noms 
d'auteur vers le format "Jean Dupont" si on le souhaite.



Listing des saisies erronées
-------------------------------------
### A corriger: Plusieurs auteurs mélangés
    Colombini, Monti, Jolanda
    Cermeño Xosé, Uhia Manuel->Uhia Manuel Cermeño Xosé
    Schartz, Irena, Stehr, Frederic->Frederic  Stehr  Irena Schartz
    Le Bloas, Renée, Robin, Pascal
    Rius, Maria, Parramon, JM

### A corriger
    May d'alençon (mettre des majuscules. Corriger l'auteur dans tous ses livres pour une unification)
    Feutre Fulda, France (supprimer la virgule, c'est un nom d'entreprise)
    K. Dubois, Claude (en vrai: Dubois, Claude K.)
    Solé Vendrell , Carme (supprimer espace inutile)
    Vendrell, Carme Solé (mettre Solé Vendrell, Carme)
    Vendrell Solé, Carme (mettre Solé Vendrell, Carme)
    Idatte, Jean Pierre (mettre tiret nom composé)
    Dumont-Le Cornec, Elisabeth (Il manque un tiret ou il y en a un en trop)
    Jacob et Wilhem (Grimm?)
    Espinassous, louis (La majuscule à Louis)
    Lung-Fou, Marie Thérèse->Marie Thérèse Lung-Fou (mettre le tiret)
    Versini, Roussel Anne (mettre le tiret entre roussel et anne?)
    Pennac (mettre Daniel Pennac)
    Guion,  Jeanine et Jean (supprimer espace en trop après virgule)
    Englebert, Jean Luc (tiret nom composé)
    Pertuzé, Joan Claudi (enlever la traduction du prénom : c'est Jean-Claude)
    Boujon, Claudi (idem)
    Dumeaux M.-O. (rajouter la virgule séparatrice nom prénom)
    Maria Parramón, Josep(le nom est "Parramon tout seul)
    JM Parramon (mettre Josep Maria Pararamon?)
    M Lamigeon
    D Madier-Daubà
    J Wilkon
    JJ Pugi
    A Saumon
    F Fijact
    L Daubà
    PJ Lynch
    H Moers
    M.W Browne
    A.J Wood
