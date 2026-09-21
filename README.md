Fonctionnement du programme
  1 - Installer les dépendane a l'aide du fichier requirement.txt
  2 - Éxécuter main.py
  
Modification possible
  A la base le programme éxécute 10 fois les 3 algorythme sur toute les fichier présent dans input-Ex1 qui ce situe dnas le dosier parent du dosier d'éxécution pour changer cela il suffit de modifier la variable global : DOSSIER_PROJET = Path(__file__).parent
  DOSSIER_INPUTS = DOSSIER_PROJET.parent / "input-Ex1".
  Il est aussi possible d'éxécuter les 3 algorythme 10 fois sur un seul fichier en donnant en argument le chemin ver le fichier a main.py

Explication des fichier d'algorythme
  Les fichier résultat des algorythme ce retrouve dans le dossier resultats /Nom fichier original/essais.txt dans le même dosier que main.py

  Le fichier de chaque algorythme est coposer de la même mannière 
  Les première ligne contienne : Numéros ittération Nombre d'élément dans la list frontiêre
  L'avant dernière ligne contien le nombre d'éxploration éffectuer
  La dernière ligne contien le temps d'éxécution
