import numpy as np
import numpy.typing as npt
from timeit import default_timer as timer
import random
from resultat import Resultat
from seekAlgorithme import SeekAlgorithme

Case = tuple[int, int]
Mouvement = tuple[int, int, int]


class HillClimbingSearch(SeekAlgorithme):

    def cases_libres_par_ligne(self, sudoku: npt.NDArray[np.int32]) -> list[list[int]]:
        return [[c for c in range(9) if sudoku[l, c] == 0] for l in range(9)]

    def etat_initial(self, sudoku: npt.NDArray[np.int32], libres: list[list[int]]) -> npt.NDArray[np.int32]:
        grille = sudoku.copy()
        for l in range(9):
            presents = set(sudoku[l][sudoku[l] != 0].tolist())
            manquants = [v for v in range(1, 10) if v not in presents]
            random.shuffle(manquants)
            grille[l, libres[l]] = manquants
        return grille

    def conflits_case(self, grille: npt.NDArray[np.int32], ligne: int, colonne: int) -> int:
        v = grille[ligne, colonne]
        l0, c0 = 3 * (ligne // 3), 3 * (colonne // 3)
        return int((grille[ligne] == v).sum()
                   + (grille[:, colonne] == v).sum()
                   + (grille[l0:l0 + 3, c0:c0 + 3] == v).sum()) - 3

    def nombre_conflits(self, grille: npt.NDArray[np.int32]) -> int:
        return sum(self.conflits_case(grille, l, c) for l in range(9) for c in range(9)) // 2

    def valeur(self, grille: npt.NDArray[np.int32]) -> int:
        return -self.nombre_conflits(grille)

    def variables_en_conflit(self, grille: npt.NDArray[np.int32], libres: list[list[int]]) -> list[Case]:
        return [(l, c) for l in range(9) if len(libres[l]) >= 2
                for c in libres[l] if self.conflits_case(grille, l, c) > 0]

    def successeurs(self, grille: npt.NDArray[np.int32], libres: list[list[int]]) -> list[Mouvement]:
        mouvements: set[Mouvement] = set()
        for l, c in self.variables_en_conflit(grille, libres):
            for c2 in libres[l]:
                if c2 != c:
                    mouvements.add((l, min(c, c2), max(c, c2)))
        return list(mouvements)

    def variation_conflits(self, grille: npt.NDArray[np.int32], ligne: int, c1: int, c2: int) -> int:
        avant = self.conflits_case(grille, ligne, c1) + self.conflits_case(grille, ligne, c2)
        grille[ligne, c1], grille[ligne, c2] = grille[ligne, c2], grille[ligne, c1]
        apres = self.conflits_case(grille, ligne, c1) + self.conflits_case(grille, ligne, c2)
        grille[ligne, c1], grille[ligne, c2] = grille[ligne, c2], grille[ligne, c1]
        return apres - avant

    def meilleur_successeur(self, current: npt.NDArray[np.int32], valeur_current: int,
                            mouvements: list[Mouvement]) -> tuple[int, Mouvement]:
        meilleure_valeur: int = -10 ** 9
        meilleurs: list[Mouvement] = []

        for l, c1, c2 in mouvements:
            valeur_successeur = valeur_current - self.variation_conflits(current, l, c1, c2)
            if valeur_successeur > meilleure_valeur:
                meilleure_valeur, meilleurs = valeur_successeur, [(l, c1, c2)]
            elif valeur_successeur == meilleure_valeur:
                meilleurs.append((l, c1, c2))

        return meilleure_valeur, random.choice(meilleurs)

    def hill_climbing(self, sudoku: npt.NDArray[np.int32],
                      historique: list[tuple[int, int]]) -> tuple[npt.NDArray[np.int32], int, int, int]:
        libres = self.cases_libres_par_ligne(sudoku)

        current = self.etat_initial(sudoku, libres)
        valeur_current = self.valeur(current)

        iterations = 0
        voisins = 0
        historique.append((iterations, -valeur_current))

        while True:
            mouvements = self.successeurs(current, libres)
            if not mouvements:
                return current, valeur_current, iterations, voisins

            valeur_neighbor, (l, c1, c2) = self.meilleur_successeur(current, valeur_current, mouvements)
            voisins += len(mouvements)
            neighbor = current.copy()
            neighbor[l, c1], neighbor[l, c2] = neighbor[l, c2], neighbor[l, c1]

            if valeur_neighbor <= valeur_current:
                return current, valeur_current, iterations, voisins

            current, valeur_current = neighbor, valeur_neighbor
            iterations += 1
            historique.append((iterations, -valeur_current))

    def hill_climbing_resolve(self, sudoku: npt.NDArray[np.int32], graine: int | None = None) -> Resultat:
        if graine is not None:
            random.seed(graine)

        start: float = timer()
        historique: list[tuple[int, int]] = []

        grille, valeur, iterations, voisins = self.hill_climbing(sudoku, historique)

        conflits = -valeur
        resolu = conflits == 0

        return Resultat(grille if resolu else None, grille, timer() - start, iterations, 0,
                        resolu, conflits, historique, voisins)