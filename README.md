# ObsidianToWebsite
Ce projet a pour objectifs de :
- proposer une méthode pour traduire du Markdown en HTML 
- partager des fiches de révisions écrites en Markdown 

Le site étant encore en développement, le server est régulièrement inaccessible, mais, si il est en ligne vous pouvez y acceder[ici](http://5.135.111.214:6969/index.md). 

# Test Local 
Si le server n'est pas accessible, ou si vous voulez y avoir acces sans internet, il est possible de le lancer en local. 
Le server est en python, mais n'utilise a ce jour aucune librairie tierce. 

## Procédure d'installation 
Ouvrez l'invité de commande, et dirigez vous dans un dossier qui vous convient.
Ensuite, il vous faut cloner les projets (respectivement celui-ci, ainsi que [Revisions](https://github.com/Alpagateau/Revisions))
Pour ce faire, entrez ces commandes :
```bash 
git clone https://github.com/Alpagateau/ObsidianToWebsite 
cd ObsidianToWebsite 
git clone https://github.com/Alpagateau/Revisions 
```

Ensuite, il suffit de lancer le server :
```bash 
python main.py 
```
## Accès au site local 
Pour acceder au site, il vous suffit de `Ctrl + Click` sur l'url imprimé par le programme, ou d'ouvrir votre navigateur et d'entrer l'url `http://localhost:6969/index.md`. 

# Structure du projet 
Le fichier principal est `main.py` qui contient toutes les règles de redirection du server, ainsi que la totalité de la logique du server lui meme. 
Celui-ci dépend de quatres scripts, tous dans le sous dossier `./parser`. 

# Information importantes 
Dans le but de rendre le plus fidèlement possible les notes prises avec Obsidian, les moteurs de rendus sont les meme. C'est a dire que :
- Mathjax est utilisé pour le rendu des équations
- highlight.js pour les morceaux de code 
- Mermaid pour les schémas (a implémenter)

# Roadmap
A lot still needs to be done. Some of the features i want to add to the websites are :
1. A graph view (like obsidian)
2. A file tree, showing all the notes

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/alpa_)
