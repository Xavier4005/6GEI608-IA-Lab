#Xavier

import PuzzleTree, PuzzleNode
from abc import ABC, abstractmethod

class SeekAlgorithm:

    _iteration_frontiere : list[(int,int)]
    _number_state_explore : int
    _execute_time : float


    def __init__(self):
        return

    @classmethod
    @abstractmethod
    def seek(self, tree : PuzzleTree):
        pass

    #Permet de générer les noeud enfant du noeud donnée. voir diabot cours 2 p.33
    def explore(self, node : PuzzleNode):
        pass