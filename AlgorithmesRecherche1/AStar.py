#Eliel

from SeekAlgorithm import SeekAlgorithm
from PuzzleTree import PuzzleTree
from PuzzleNode import PuzzleNode

import numpy.typing as npt
import numpy as np

class AStar(SeekAlgorithm):
    
    def seek(self, tree: PuzzleTree, objectif: npt.NDArray[np.int32]) -> PuzzleNode | None:
    #Heuristique a utiliser Max(nombre de carré mal placer, Distane de Manhattan)
        pass


    def heuristique(node : PuzzleNode) -> int:
        pass