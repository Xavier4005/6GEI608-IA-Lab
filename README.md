# Documentation du programme

## Fonctionnement du programme

1. **Installer les dépendances** à l'aide du fichier `requirements.txt`
2. **Exécuter** `main.py`

---

## Modifications possibles

Par défaut, le programme exécute **10 fois** les 3 algorithmes sur tous les fichiers présents dans `input-Ex1` (situé dans le dossier parent du dossier d'exécution). 

### 1. Modifier le dossier source
Pour changer ce comportement, il suffit de modifier les variables globales suivantes :

```python
DOSSIER_PROJET = Path(__file__).parent
DOSSIER_INPUTS = DOSSIER_PROJET.parent / "input-Ex1"
```

### 2. Exécuter sur un seul fichier
Il est également possible d'exécuter les 3 algorithmes 10 fois sur un seul fichier en passant le chemin vers le fichier en argument à `main.py`.

---

## Explication des fichiers d'algorithme

Les fichiers de résultats des algorithmes se trouvent dans le répertoire :
`resultats/[Nom du fichier original]/essais.txt` (dans le même dossier que `main.py`).

Le fichier de chaque algorithme est composé de la même manière :
* **Premières lignes :** `Numéro d'itération` | `Nombre d'éléments dans la liste frontière`
* **Avant-dernière ligne :** Nombre d'explorations effectuées
* **Dernière ligne :** Temps d'exécution

## Ce qui a été appris pendant le laboratoire
Les nouvelles informations apprises lors de ce laboratoire concernent la manière d'implémenter en Python trois algorithmes de recherche (**BFS**, **DFS** et **IDDFS**) ainsi que leurs différences :

* **BFS (Breadth-First Search) :** Il permet de trouver le chemin le plus court (avec un nombre d'étapes réduit).
* **DFS (Depth-First Search) :** Il ne donne pas forcément le meilleur chemin ; les parcours trouvés sont souvent très longs.
* **IDDFS (Iterative Deepening Depth-First Search) :** Il donne quasiment le même chemin que BFS. Cependant, lorsqu'aucun résultat n'est disponible, il prend plus de temps pour confirmer l'absence de solution, car il doit explorer le graphe jusqu'à la profondeur maximale à chaque itération.
