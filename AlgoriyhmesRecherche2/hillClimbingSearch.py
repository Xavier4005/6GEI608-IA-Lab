import numpy as np
import numpy.typing as npt
from timeit import default_timer as timer
from math import inf
import random
from resultat import Resultat
from itertools import combinations
from seekAlgorithme import SeekAlgorithme

MAX_REDEMARRAGES : int = 100          # nombre maximal de redémarrages aléatoires

class HillClimbingSearch(SeekAlgorithme):


    def doublons(self,valeurs : npt.NDArray[np.int32]) -> int:

        return 9 - len(set(valeurs.tolist()))


    def bloc_de(self,grille : npt.NDArray[np.int32], ligne : int, colonne : int) -> npt.NDArray[np.int32]:
        l0, c0 = 3 * (ligne // 3), 3 * (colonne // 3)
        return grille[l0:l0 + 3, c0:c0 + 3].ravel()


    def cout_local(self,grille : npt.NDArray[np.int32], ligne : int, c1 : int, c2 : int) -> int:

        cout = self.doublons(grille[:, c1]) + self.doublons(grille[:, c2])
        cout += self.doublons(self.bloc_de(grille, ligne, c1))
        if c1 // 3 != c2 // 3:
            cout += self.doublons(self.bloc_de(grille, ligne, c2))
        return cout


    def cases_libres_par_ligne(self,sudoku : npt.NDArray[np.int32]) -> list[list[int]]:

        return [[c for c in range(9) if sudoku[l, c] == 0] for l in range(9)]


    def remplir_lignes(self,sudoku : npt.NDArray[np.int32], libres : list[list[int]]) -> npt.NDArray[np.int32]:

        grille = sudoku.copy()
        for l in range(9):
            presents = set(sudoku[l][sudoku[l] != 0].tolist())
            manquants = [v for v in range(1, 10) if v not in presents]
            random.shuffle(manquants)
            grille[l, libres[l]] = manquants
        return grille


    def successeurs(self,libres : list[list[int]]) -> list[tuple[int, int, int]]:
        return [(l, c1, c2) for l in range(9) for c1, c2 in combinations(libres[l], 2)]


    def meilleur_successeur(self,grille : npt.NDArray[np.int32],
                            mouvements : list[tuple[int, int, int]]) -> tuple[int, tuple[int, int, int]]:
        meilleur_delta : int = 10 ** 9
        meilleurs : list[tuple[int, int, int]] = []

        for l, c1, c2 in mouvements:
            avant = self.cout_local(grille, l, c1, c2)
            grille[l, c1], grille[l, c2] = grille[l, c2], grille[l, c1]
            delta = self.cout_local(grille, l, c1, c2) - avant
            grille[l, c1], grille[l, c2] = grille[l, c2], grille[l, c1]

            if delta < meilleur_delta:
                meilleur_delta, meilleurs = delta, [(l, c1, c2)]
            elif delta == meilleur_delta:
                meilleurs.append((l, c1, c2))

        return meilleur_delta, random.choice(meilleurs)


    def monter(self,grille : npt.NDArray[np.int32], mouvements : list[tuple[int, int, int]],
            historique : list[tuple[int, int]], iteration_depart : int) -> tuple[int, int, int]:
        cout = self.get_number_conflic(grille)
        iterations = 0
        voisins = 0
        historique.append((iteration_depart, cout))

        while mouvements:
            delta, (l, c1, c2) = self.meilleur_successeur(grille, mouvements)
            voisins += len(mouvements)

            if delta >= 0:
                break

            grille[l, c1], grille[l, c2] = grille[l, c2], grille[l, c1]
            cout += delta
            iterations += 1
            historique.append((iteration_depart + iterations, cout))

        return cout, iterations, voisins


    def hill_climbing_resolve(self, sudoku : npt.NDArray[np.int32], graine : int | None = None) -> Resultat:

        if graine is not None:
            random.seed(graine)

        libres = self.cases_libres_par_ligne(sudoku)
        mouvements = self.successeurs(libres)

        start : float = timer()
        iterations : int = 0
        voisins : int = 0
        meilleure_grille = sudoku.copy()
        meilleur_cout : float = inf
        historique : list[tuple[int, int]] = []

        for redemarrage in range(MAX_REDEMARRAGES):
            grille = self.remplir_lignes(sudoku, libres)
            cout, it, v = self.monter(grille, mouvements, historique, iterations)
            iterations += it
            voisins += v

            if cout < meilleur_cout:
                meilleur_cout = cout
                meilleure_grille = grille.copy()

            if cout == 0:
                return Resultat(grille, grille, timer() - start, iterations, redemarrage,
                                True, 0, historique, voisins)

        return Resultat(None, meilleure_grille, timer() - start, iterations, MAX_REDEMARRAGES,
                        False, int(meilleur_cout), historique, voisins)