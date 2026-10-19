from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
import numpy as np
import numpy.typing as npt
from timeit import default_timer as timer
from math import inf
import random
from resultat import Resultat
from IO import IO 

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


MAX_REDEMARRAGES : int = 100          # nombre maximal de redémarrages aléatoires
MAX_SANS_AMELIORATION : int = 2_000   # voisins consécutifs sans amélioration
PAS_HISTORIQUE : int = 1


def doublons(valeurs : npt.NDArray[np.int32]) -> int:

    return 9 - len(set(valeurs.tolist()))


def bloc_de(grille : npt.NDArray[np.int32], ligne : int, colonne : int) -> npt.NDArray[np.int32]:
    l0, c0 = 3 * (ligne // 3), 3 * (colonne // 3)
    return grille[l0:l0 + 3, c0:c0 + 3].ravel()


def cout_local(grille : npt.NDArray[np.int32], ligne : int, c1 : int, c2 : int) -> int:

    cout = doublons(grille[:, c1]) + doublons(grille[:, c2])
    cout += doublons(bloc_de(grille, ligne, c1))
    if c1 // 3 != c2 // 3:
        cout += doublons(bloc_de(grille, ligne, c2))
    return cout


def cases_libres_par_ligne(sudoku : npt.NDArray[np.int32]) -> list[list[int]]:

    return [[c for c in range(9) if sudoku[l, c] == 0] for l in range(9)]


def remplir_lignes(sudoku : npt.NDArray[np.int32], libres : list[list[int]]) -> npt.NDArray[np.int32]:

    grille = sudoku.copy()
    for l in range(9):
        presents = set(sudoku[l][sudoku[l] != 0].tolist())
        manquants = [v for v in range(1, 10) if v not in presents]
        random.shuffle(manquants)
        grille[l, libres[l]] = manquants
    return grille


def hill_climbing_resolve(sudoku : npt.NDArray[np.int32], graine : int | None = None) -> Resultat:

    if graine is not None:
        random.seed(graine)

    libres = cases_libres_par_ligne(sudoku)
    lignes_mutables = [l for l in range(9) if len(libres[l]) >= 2]

    start : float = timer()
    nombre_iteration : int = 0
    meilleure_grille = sudoku.copy()
    meilleur_cout : float = inf
    redemarrage : int = 0
    historique : list[tuple[int, int]] = []

    while redemarrage < MAX_REDEMARRAGES:
        grille = remplir_lignes(sudoku, libres)
        cout = get_number_conflic(grille)
        sans_amelioration = 0

        while cout > 0 and sans_amelioration < MAX_SANS_AMELIORATION and lignes_mutables:
            nombre_iteration += 1

            # 1. Voisin aléatoire : échange de deux cases libres d'une même ligne
            l = random.choice(lignes_mutables)
            c1, c2 = random.sample(libres[l], 2)

            avant = cout_local(grille, l, c1, c2)
            grille[l, c1], grille[l, c2] = grille[l, c2], grille[l, c1]
            delta = cout_local(grille, l, c1, c2) - avant

            # 2. Accepter si le coût ne remonte pas (delta == 0 : mouvement latéral)
            if delta <= 0:
                cout += delta
                sans_amelioration = 0 if delta < 0 else sans_amelioration + 1
            else:
                # 3. Sinon annuler l'échange
                grille[l, c1], grille[l, c2] = grille[l, c2], grille[l, c1]
                sans_amelioration += 1

            if nombre_iteration % PAS_HISTORIQUE == 0:
                historique.append((nombre_iteration, cout))

        if cout < meilleur_cout:
            meilleur_cout = cout
            meilleure_grille = grille.copy()

        if cout == 0:
            end : float = timer()
            return Resultat(grille, grille, end - start, nombre_iteration, redemarrage, True, 0,
                            historique)

        # Optimum local : redémarrage à partir d'un nouveau remplissage aléatoire
        redemarrage += 1

    end = timer()
    return Resultat(None, meilleure_grille, end - start, nombre_iteration,
                    redemarrage, False, int(meilleur_cout), historique)

def est_valide(grille : npt.NDArray[np.int32], puzzle : npt.NDArray[np.int32]) -> bool:
    """Vérifie les trois règles du Sudoku et que les cases du puzzle sont intactes."""
    figees = puzzle != 0
    return get_number_conflic(grille) == 0 and bool(np.all(grille != 0)) \
        and bool(np.array_equal(grille[figees], puzzle[figees]))

DOSSIER_PUZZLES : Path = Path(__file__).parent / "puzzles"
DOSSIER_RESULTATS : Path = Path(__file__).parent / "resultats"


NB_EXECUTIONS : int = 10

ALGORITHMES : dict[str, Callable[..., Resultat]] = {
    "hill_climbing": hill_climbing_resolve,
}


def main():
    puzzles = IO.read_all(DOSSIER_PUZZLES)
    print(f"{len(puzzles)} puzzle(s) chargé(s) depuis « {DOSSIER_PUZZLES} »")

    for nom_algorithme, resoudre in ALGORITHMES.items():
        print(f"\n=== {nom_algorithme} ===")

        for puzzle in puzzles:
            difficulte = puzzle.metadonnees.get("Difficulty", "?")

            for numero in range(1, NB_EXECUTIONS + 1):
                res = resoudre(puzzle.grille, graine=numero)

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

