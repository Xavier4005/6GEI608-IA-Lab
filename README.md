# Vidéo de démonstration : [Visionner la vidéo Panopto](https://uqac.ca.panopto.com/Panopto/Pages/Viewer.aspx?id=5c030e41-a871-4294-8617-b4ee018333ca)

# Documentation du programme

## Fonctionnement du programme

1. **Installer les dépendances** à l'aide du fichier `requirements.txt`.
2. **Exécuter** `main.py`.

---

## AlgorithmesRecherche1

Par défaut, le programme exécute **10 fois** les 4 algorithmes sur tous les fichiers présents dans `input-Ex1` (situé dans le dossier parent du dossier d'exécution). 

### 1. Modifier le dossier source
Pour changer ce comportement, il suffit de modifier les variables globales suivantes :

```python
DOSSIER_PROJET = Path(__file__).parent
DOSSIER_INPUTS = DOSSIER_PROJET.parent / "input-Ex1"
```

### 2. Exécuter sur un seul fichier
Il est également possible d'exécuter les 4 algorithmes 10 fois sur un seul fichier en passant le chemin vers celui-ci en argument à `main.py`.

---

## AlgorithmesRecherche2

Le programme exécute **10 fois** les 2 algorithmes sur tous les fichiers présents dans `puzzles` (situé dans le dossier d'exécution). 

---

## Explication des fichiers de résultats

### AlgorithmesRecherche1

Les fichiers de résultats des algorithmes se trouvent dans le répertoire :
`resultats/[Nom du fichier original]/essais.txt` (dans le même dossier que `main.py`).

Le fichier de chaque algorithme est composé de la manière suivante :
- **Premières lignes :** `Numéro d'itération` | `Nombre d'éléments dans la liste frontière`
- **Avant-dernière ligne :** Nombre d'explorations effectuées
- **Dernière ligne :** Temps d'exécution

### AlgorithmesRecherche2

Les fichiers de résultats des algorithmes se trouvent dans le répertoire :
`resultats/[Nom du fichier original]/[nom_algorithme]/`

Ces résultats sont constitués de deux fichiers :
- `execution.txt`
- `solution.txt`

Le fichier **`execution.txt`** contient toutes les itérations de l'algorithme, le nombre de conflits à chaque exécution ainsi que le nombre total d'exécutions. Il est composé de la manière suivante :
- **Premières lignes :** `Numéro d'itération` | `Nombre d'éléments dans la liste frontière`
- **Avant-dernière ligne :** Nombre d'explorations effectuées
- **Dernière ligne :** Temps d'exécution

Le fichier **`solution.txt`** contient la solution partielle ou totale trouvée pour le sudoku. Il est composé de la manière suivante :
- **Première ligne :** Nom du sudoku
- **Deuxième ligne :** Difficulté du sudoku
- **Troisième ligne :** Indique s'il est résolu ou non
- **Quatrième ligne :** Nombre de fois que l'algorithme a redémarré totalement
- **Cinquième ligne :** Nombre final de conflits
- **Dernières lignes :** Résultat obtenu

---

## Ce qui a été appris pendant le laboratoire

Nous avons appris que l'utilisation d'algorithmes informés dotés de bonnes heuristiques permet de réduire drastiquement le nombre d'étapes et le temps de résolution des problèmes par rapport aux algorithmes non informés. La comparaison de l'algorithme A* avec BFS, DFS et IDF cela montre clairement que A* est supérieur pour résoudre les problèmes de recherche d'états.

Ensuite, nous avons pu voir qu'il était possible de résoudre un problème plus complexe comme celui du sudoku à l'aide d'algorithmes tels que le *Hill Climbing* et l'algorithme génétique. Cependant, nous avons aussi constaté que ces derniers sont très inconstants dans la résolution : ils peuvent rester bloqués sur des minima locaux pendant longtemps et être obligés de redémarrer souvent pour atteindre la solution optimale. Cela peut avoir un impact majeur sur le temps de convergence de l'algorithme.
