#Xavier

from puzzleNode import PuzzleNode
from puzzleTree import PuzzleTree
from abc import ABC, abstractmethod
import numpy.typing as npt
import numpy as np

MATRIX_DIM = 2

class SeekAlgorithm(ABC):
    _iteration_frontiere : list[tuple[int,int]]
    _number_state_explore : int
    _execute_time : float

    def __init__(self):
        return

    @abstractmethod
    def seek(self, tree : PuzzleTree, objectif : npt.NDArray[np.int32]):
        pass

    #Permet de générer les noeud enfant du noeud donnée. voir diabot cours 2 p.33
    def explore(self, node : PuzzleNode):
        # Aller cherche la position du zéro dasn la matrice
        zero_row, zero_columns = node.zero_position
        # création du noeud en haut
        if node.zero_position[1] < MATRIX_DIM:
            new_data = node.data.copy()

            new_data[zero_row, zero_columns] = new_data[zero_row + 1, zero_columns]
            new_data[zero_row + 1, zero_columns] = 0
            node.child_nodes.append(PuzzleNode(new_data,  (zero_row + 1, zero_columns), node))
        # création du noeud en bas
        if zero_row > 0:
            new_data = node.data.copy()

            new_data[zero_row, zero_columns] = new_data[zero_row - 1, zero_columns]
            new_data[zero_row - 1, zero_columns] = 0
            node.child_nodes.append(PuzzleNode(new_data,  (zero_row - 1, zero_columns), node))

        # création du noeud a droite
        if zero_columns < MATRIX_DIM:
            new_data = node.data.copy()

            new_data[zero_row, zero_columns] = new_data[zero_row, zero_columns + 1]
            new_data[zero_row, zero_columns + 1] = 0
            node.child_nodes.append(PuzzleNode(new_data,  (zero_row, zero_columns + 1), node))

        # création du noeud a gauche
        if zero_columns > 0:
            new_data = node.data.copy()

            new_data[zero_row, zero_columns] = new_data[zero_row, zero_columns - 1]
            new_data[zero_row, zero_columns - 1] = 0
            node.child_nodes.append(PuzzleNode(new_data,  (zero_row, zero_columns - 1), node))
        

    def verify(self, node : PuzzleNode, objectif : npt.NDArray[np.int32]) -> bool:
        return np.array_equal(node.data, objectif)