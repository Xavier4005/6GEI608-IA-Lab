import numpy as np
import numpy.typing as npt



class Resultat:
    solution: npt.NDArray[np.int32] | None   # grille résolue, ou None en cas d'échec
    meilleure_grille: npt.NDArray[np.int32]   # meilleure grille rencontrée
    temps: float
    iterations: int                           
    redemarrages: int
    resolu: bool
    conflits_finaux: int
    historique: list[tuple[int, int]]
    voisins_evalues: int

    def __init__(self, solution: npt.NDArray[np.int32] | None, meilleure_grille: npt.NDArray[np.int32],  temps: float, iterations: int, redemarrages: int, resolu: bool, conflits_finaux: int, voisins_evalues : int = 0):
        self.solution = solution
        self.meilleure_grille = meilleure_grille
        self.temps = temps
        self.iterations = iterations
        self.redemarrages = redemarrages
        self.resolu = resolu
        self.conflits_finaux = conflits_finaux
        self.historique = list[tuple[int,int]]()
        self.voisins_evalues = voisins_evalues