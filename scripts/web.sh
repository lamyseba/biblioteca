#!/bin/bash

# Compile le fichier xml de tellico pour en faire une page web
# Envoie ensuite par ftp cette page web sur le serveur calandreta.
# Note: l'envoi ftp ne marche que si il existe dans la racine
# du home utilisateur un fichier nommé .netrc qui contient les
# lignes suivantes:
### machine ftp.de.la.calandreta.com
### login user
### password secret

# Si la commande de génération de la page se passe mal, il faut sortir du
# script avant l'upload.
set -e

# On enregistre la date de mise à jour
DATE=$(date +"%d %b %Y")

# Dezippe le fichier XML de tellico
unzip -p ~/Bibli/inventaire.tc tellico.xml | \
\
# Compile le xml pour faire une page web enregistrée dans /tmp/index.html
xsltproc --novalid --param "column-names" "'id title author editor language genre cote nb-ex notes'" \
        --param "cdate" "'$DATE'" \
        ~/Bibli/scripts/templates/web.xsl \
        - > /tmp/index.html

# Envoie le fichier sur le serveur calandreta
echo put /tmp/index.html /bibli/index.html | ftp ftp.cluster010.hosting.ovh.net

