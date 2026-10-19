from abc import ABC
import numpy as np
import numpy.typing as npt

class SeekAlgorithme(ABC):

    def get_number_conflic(self,sudoku : npt.NDArray[np.int32]) -> int:
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