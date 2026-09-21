#Xavier

from SeekAlgorithm import SeekAlgorithm
from puzzleTree import PuzzleTree
from PuzzleNode import PuzzleNode
from timeit import default_timer as timer
import numpy.typing as npt
import numpy as np
from collections import deque
from copy import deepcopy

class IDF(SeekAlgorithm):

    def seek(self, tree: PuzzleTree, objectif: npt.NDArray[np.int32]) -> PuzzleNode | None:
            max_depth: int = 40
            iteration: int = 0
            start: float = timer()

            for current_max_depth in range(max_depth):
                frontiere: deque[tuple[PuzzleNode, int]] = deque()
                frontiere.append((tree.root, 0))

                visites: set[bytes] = {tree.root.data.tobytes()}

                while len(frontiere) != 0:
                    self._iteration_frontiere.append((iteration, len(frontiere)))
                    iteration += 1

                    actual_node, actual_depth = frontiere.pop()

                    if self.verify(actual_node, objectif):
                        end: float = timer()
                        self._execute_time = end - start
                        self._number_state_explore = iteration
                        return actual_node

                    if actual_depth < current_max_depth:
                        self.explore(actual_node)
                        for child in actual_node.child_nodes:
                            cle: bytes = child.data.tobytes()
                            if cle not in visites:
                                visites.add(cle)
                                frontiere.append((child, actual_depth + 1))

            return None

                


            




        
