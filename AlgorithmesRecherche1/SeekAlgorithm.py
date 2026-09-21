#Xavier

from PuzzleNode import PuzzleNode
from puzzleTree import PuzzleTree
from abc import ABC, abstractmethod
import numpy.typing as npt
import numpy as np

MATRIX_DIM = 3

class SeekAlgorithm(ABC):
    _iteration_frontiere : list[tuple[int,int]]
    _number_state_explore : int
    _execute_time : float

    def __init__(self) -> None:
        self._iteration_frontiere: list[tuple[int, int]] = []
        self._number_state_explore: int = 0
        self._execute_time: float = 0.0

    @abstractmethod
    def seek(self, tree : PuzzleTree, objectif : npt.NDArray[np.int32]) -> PuzzleNode | None:
        pass

    #Permet de générer les noeud enfant du noeud donnée. voir diabot cours 2 p.33
    def explore(self, node: PuzzleNode):
        if len(node.child_nodes) != 0:
            return

        zero_row, zero_col = node.zero_position

        # 1. Déplacement de la case vide vers le HAUT (ligne au-dessus)
        if zero_row > 0:
            new_data = node.data.copy()
            new_data[zero_row, zero_col] = new_data[zero_row - 1, zero_col]
            new_data[zero_row - 1, zero_col] = 0
            node.child_nodes.append(PuzzleNode(new_data, (zero_row - 1, zero_col), node))

        # 2. Déplacement de la case vide vers le BAS (ligne en-dessous)
        if zero_row < MATRIX_DIM - 1:
            new_data = node.data.copy()
            new_data[zero_row, zero_col] = new_data[zero_row + 1, zero_col]
            new_data[zero_row + 1, zero_col] = 0
            node.child_nodes.append(PuzzleNode(new_data, (zero_row + 1, zero_col), node))

        # 3. Déplacement de la case vide vers la GAUCHE (colonne précédente)
        if zero_col > 0:
            new_data = node.data.copy()
            new_data[zero_row, zero_col] = new_data[zero_row, zero_col - 1]
            new_data[zero_row, zero_col - 1] = 0
            node.child_nodes.append(PuzzleNode(new_data, (zero_row, zero_col - 1), node))

        # 4. Déplacement de la case vide vers la DROITE (colonne suivante)
        if zero_col < MATRIX_DIM - 1:
            new_data = node.data.copy()
            new_data[zero_row, zero_col] = new_data[zero_row, zero_col + 1]
            new_data[zero_row, zero_col + 1] = 0
            node.child_nodes.append(PuzzleNode(new_data, (zero_row, zero_col + 1), node))
        

    def verify(self, node : PuzzleNode, objectif : npt.NDArray[np.int32]) -> bool:
        return np.array_equal(node.data, objectif)