from pathlib import Path
import numpy as np
import numpy.typing as npt
from IO import IO 
from seekAlgorithme import SeekAlgorithme
from hillClimbingSearch import HillClimbingSearch
from geneticSearch import GeneticSearch



def get_number_conflic(sudoku : npt.NDArray[np.int32]) -> int:
    lignes : list[int] = [0] * 9
    colonnes : list[int] = [0] * 9
    blocs : list[int] = [0] * 9

    nb_conflit : int = 0

    for (ligne, colonne), valeur in np.ndenumerate(sudoku):
        valeur_py = int(valeur)

        if valeur_py == 0:
            continue

        bloc : int = 3 * (ligne // 3) + (colonne // 3)

        masque : int = 1 << (valeur_py - 1)

        # Teste pour les lignes
        if (lignes[ligne] & masque) == 0:
            lignes[ligne] |=  masque
        else:
            nb_conflit += 1

        # Teste pour les colonnes
        if (colonnes[colonne] & masque) == 0:
            colonnes[colonne] |=  masque
        else:
            nb_conflit += 1

        # Teste pour les blocs
        if (blocs[bloc] & masque) == 0:
            blocs[bloc] |= masque
        else:
            nb_conflit += 1


    return nb_conflit

# Hill climbing (Eliel)

def est_valide(grille : npt.NDArray[np.int32], puzzle : npt.NDArray[np.int32]) -> bool:
    """Vérifie les trois règles du Sudoku et que les cases du puzzle sont intactes."""
    figees = puzzle != 0
    return get_number_conflic(grille) == 0 and bool(np.all(grille != 0)) \
        and bool(np.array_equal(grille[figees], puzzle[figees]))

DOSSIER_PUZZLES : Path = Path(__file__).parent / "puzzles"
DOSSIER_RESULTATS : Path = Path(__file__).parent / "resultats"


NB_EXECUTIONS : int = 10

ALGORITHMES : dict[str, SeekAlgorithme] = {
    #"hill_climbing": HillClimbingSearch(),
    "geneic" : GeneticSearch()
}


def main():
    puzzles = IO.read_all(DOSSIER_PUZZLES)
    print(f"{len(puzzles)} puzzle(s) chargé(s) depuis « {DOSSIER_PUZZLES} »")

    for nom_algorithme, algorithme in ALGORITHMES.items():
        print(f"\n=== {nom_algorithme} ===")

        for puzzle in puzzles:
            difficulte = puzzle.metadonnees.get("Difficulty", "?")

            for numero in range(1, NB_EXECUTIONS + 1):

                if type(algorithme) is HillClimbingSearch:
                    res = algorithme.hill_climbing_resolve(puzzle.grille, graine=numero)
                elif type(algorithme) is GeneticSearch:
                    res = algorithme.genetic_resolve(puzzle.grille)
                else:
                    raise RuntimeError(f"Algorithme inconnue")
                    

                if res.resolu and not est_valide(res.solution, puzzle.grille):
                    raise RuntimeError(f"Solution invalide : {puzzle.nom}, exécution {numero}")

                IO.export_statistiques(DOSSIER_RESULTATS, puzzle.nom, nom_algorithme, numero,
                                       res.historique, res.iterations, res.temps)
                IO.write_solution(
                    DOSSIER_RESULTATS / puzzle.nom / nom_algorithme / f"solution_{numero:02d}.txt",
                    puzzle, res)

                print(f"{puzzle.nom} ({difficulte}) exéc. {numero:2d} | "
                      f"résolu : {'oui' if res.resolu else 'non'} | {res.temps:7.3f} s | "
                      f"{res.iterations:>7} itérations")

    print(f"\nStatistiques enregistrées dans « {DOSSIER_RESULTATS} »")


#[0,0] en-bas a gauche

#Eliel
#Utilisation d'une matrice 9x9 pour représenter le sudoku
# euristique hill glambing : nombre de conflit avec les autre nombre ex : 8 7 8 =  4

#Xavier
# Algorythme génétique : fitnesse même que heuristique, calcul sélection sélection fitness individue / fitnesse total génération, séparation par prorata du fitness en horizontalement

#Eliel
#IO

#Xavier
#Fonction heuristique / fitness

#Comment définir les noeud du sodoku
#
if __name__ == "__main__":
    main()