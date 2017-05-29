---
auteur: Sébastien Lamy (lamyseba arobase free.fr)
---

Norme pour la saisie des données bibliographiques
===========================================================

* **Titre** : Ce champs dispose de l'auto-complétion pour **éviter les doublons
  dans l'inventaire**.
  <div class="admonition important">
  **Si le titre existe déjà**, il faut **annuler la saisie** du livre, chercher 
  le livre existant dans l'inventaire et **mettre à  jour le nombre d'exemplaire**.</div>
* **Sous-titre** (facultatif)
* **Auteur** : Nous utilisons le format `Nom, Prénom` pour chaque auteur. On
  peut saisir une liste de plusieurs auteurs en les séparant par des `;`  
  Par exemple `Dupont, Jean; D'Agobert, Roger`. Ce choix de formattage est
  issu d'[une réflexion], mais une autre école pourrait faire un autre choix.
* **Editeur** : Correspond au copyritght © inscrit quelque part sur 
  le livre
* **Langue** : Si il y a deux langues, on les sépare par un `/`, en commençant
  par le Français.
* **Genre** : `Album`; `BD`; `Contes`; `Documentaire`; `Poésie`; `Roman`; `Théâtre`
* **Cote** : La cote de rangement du livre.
    * Si c'est un album, la cote est la première lettre du nom de l'auteur.
      Elle sera scotchée en haut à droite de la couverture.
    * Si c'est un documentaire, la cote est le code numérique du thème suivi 
      d'un espace puis du nom du thème. Elle sera imprimée sur un papier de 
      couleur verte et scotchée en bas du dos.
    * Pour les autres genre de livre, la cote est le code qui correspond au 
      genre (`C` pour les contes, `BD` pour les BDs, `R` pour les romans, `T` 
      pour le Théâtre, `P` pour la poésie), suivi d'un espace puis des trois
      première lettre du nom de l'auteur. Elle sera scotchée en bas du dos.
* **Nb ex** : Le nombre d'exemplaire du livre
* **Nb. fich. manq.** : Le nombre de fiches qu'il manque pour ce livre. Le 
  programme d'impression des fiches utilise ce nombre et le remet à zéro.
  Vérifiez si vote livre a déjà une fiche lisible. Si c'est le cas il faudra
  reporter le numéro d'inventaire sur cette fiche après enregistrement du livre.
* **Nb. cotes manq.** : Le nombre de cotes qu'il manque pour ce livre. Le 
  programme d'impression des cotes utilise ce nombre et le remet à zéro.
  Vérifier si votre livre a déjà une cote correcte (une lettre en gros sur
  la couverture pour les albums, un code au bas du dos pour les autre genres)
  
!!! important ""
    **Pensez à écrire le numéro d'inventaire sur la page de titre du livre !!**
    Si le livre a déjà une fiche, il faut aussi écrire ce numéro **sur la fiche**.
    
    Ce numéro est diponible une fois le livre enregistré dans l'inventaire. Il 
    se trouve dans la colonne `N°` de la ligne qui correspond au livre.
    
    Dans le cas où le livre a **plusieurs exemplaires**, écrire le **numéro 
    d'exemplaire** juste à coté du numéro d'inventaire **sur la page de titre du 
    livre et sur sa fiche**. Séparer par un tiret. Par exemple `177-1` pour le premier exemplaire du livre n°177, 
    `177-2` pour le second, et ainsi de suite.
[une réflexion]:format-noms-d-auteur.html