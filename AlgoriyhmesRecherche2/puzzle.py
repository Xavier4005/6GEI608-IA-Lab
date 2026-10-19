import numpy as np
import numpy.typing as npt

class Puzzle:
    nom: str
    grille: npt.NDArray[np.int32]
    metadonnees: dict[str, str]

    def __init__(self, nom : str, grille : npt.NDArray[np.int32], metadonnees : dict[str,str]):
        self.nom = nom
        self.grille = grille
        self.metadonnees = metadonnees