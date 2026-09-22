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
