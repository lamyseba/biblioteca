#/bin/bash

# Mets à jour sur github la base de donnée tellico
# Pour appeler ce script automatiquement en arrière plan
# il faut s'assurer que le push est possible sans rentrer
# de mot de passe pour l'utilisateur qui lance ce script

cd /home/calandreta/Bibli
git add inventaire.tc
git commit -m "Mise à jour de la base de donnée tellico"
git add docs/*
git commit -m "Mise à jour de la documentation"
git push origin master

