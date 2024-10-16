# ObsidianToWebsite
Ce projet a pour objectifs de :
- proposer une méthode pour traduire du Markdown en HTML 
- partager des fiches de révisions écrites en Markdown 


Le site étant encore en développement, le server est régulièrement inaccessible, mais, si il est en ligne vous pouvez y acceder [ici](https://mnadaud.fr/index.md). 
Enfin en HTTPS d'ailleur ! 

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
## Où trouver le site 
Actulellement, le site est trouvable [ici](https://mnadaud.fr/index.md). Il est important de noter que le site ne supporte pas encore l'https, et peut donc afficher un message d'erreur si vous essayer de l'ouvrir. 
Le site est complètement sans danger (si vous ne me croyez pas, regardez le code vous même). 

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

# Comment ça marche 
Chaque requète est d'abord vérifiée, puis redirigée vers le fichier correspondant. Alors, `lexer.py` découpe le fichier en une liste de symboles sémantiques. Ensuite, le `parser` transforme cette liste en un arbre sémantique (voir [Arbre de syntaxe abstraite](https://en.wikipedia.org/wiki/Abstract_syntax_tree)). 
Enfin, un `renderer` traduit cet arbre en fichier html lisisble par un moteur de recherche. 

## Table de traduction 
Ici sont les symboles traduits du markdown a l'html : 

| Markdown | Html     |
| -------- | -------- |
| `#`      | `<h1>`   |
| `##`     | `<h2>`   |
| `###`    | `<h3>`   |
| `####`   | `<h4>`   |
| `#####`  | `<h5>`   |
| `\n`     | `<br>`   |
| `*`      | `<i>`    |
| `**`     | `<b>`    |
| `==`     | `<mark>` |

# Roadmap
A lot still needs to be done. Some of the features i want to add to the websites are :
1. A graph view (like obsidian)
2. A file tree, showing all the notes

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/alpa_)
