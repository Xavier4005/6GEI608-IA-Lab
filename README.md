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
J'ai appris à formuler le 8-puzzle comme un problème de recherche : un espace d'états, des actions correspondant aux déplacements de la case vide, un état initial et un test d'objectif.
J'ai appris à reconstruire le chemin des actions en remontant les liens de parenté depuis le nœud solution jusqu'à la racine.
J'ai compris que les trois algorithmes ne diffèrent que par la structure de la frontière : une file (FIFO) pour le BFS, une pile (LIFO) pour le DFS, et une pile avec limite de profondeur croissante pour l'IDF.
J'ai constaté que le BFS et l'IDF sont optimaux, avec des solutions de alors que le DFS produit des chemins très long.
