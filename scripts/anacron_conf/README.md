Ce dossier contient la configuration d'[anacron][]. À copier dans votre `home` sous le nom `.anacron`,
avant de l'adapter à vos besoin. En supposant que c'est votre utilisateur qui va faire les commits 
github et les uploads ftp.

```bash
cp -r scripts/anacron_conf ~/.anacron
```

Pour lancer anacron au démarrage de votre session, il faudra ajouter la ligne suivant au fichier `.bashrc` de votre home:
```
# Lance anacron
anacron
```

[anacron]:http://www.delafond.org/traducmanfr/man/man8/anacron.8.html
