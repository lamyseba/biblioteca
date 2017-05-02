#/bin/bash

# Compile le fichier xml de tellico pour en faire une page web
# Envoie ensuite cette page web sur le serveur calandreta.
# Note: ce script ne marche que si il existe dans la racine
# du home utilisateur un fichier nommé .netrc qui contient les
# lignes suivantes:
### machine ftp.de.la.calandreta.com
### login user
### password secret

# Dezippe le fichier XML de tellico
unzip -p ~/Bibli/inventaire.tc tellico.xml | \
\
# Compile le xml pour faire une page web enregistrée dans /tmp/index.html
xsltproc --param "column-names" "'id title author editor language genre cote nb-ex'" \
        ~/Bibli/CodeSource/templates/web.xsl \
        - > /tmp/index.html

# Envoie le fichier sur le serveur calandreta
echo put /tmp/index.html /bibli/index.html | ftp ftp.cluster010.hosting.ovh.net
