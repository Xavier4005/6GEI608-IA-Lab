#Eliel

from SeekAlgorithm import SeekAlgorithm
from puzzleTree import PuzzleTree
from PuzzleNode import PuzzleNode
from timeit import default_timer as timer
import numpy.typing as npt
import numpy as np
from collections import deque


class BFS(SeekAlgorithm):

    def seek(self, tree: PuzzleTree, objectif: npt.NDArray[np.int32]) -> PuzzleNode | None:
        iteration: int = 0
        start: float = timer()

        frontiere: deque[PuzzleNode] = deque()
        frontiere.append(tree.root)

        visites: set[bytes] = {tree.root.data.tobytes()}

        while len(frontiere) != 0:
            self._iteration_frontiere.append((iteration, len(frontiere)))
            iteration += 1

            actual_node: PuzzleNode = frontiere.popleft()

            if self.verify(actual_node, objectif):
                self._execute_time = timer() - start
                self._number_state_explore = iteration
                return actual_node

            self.explore(actual_node)
            for child in actual_node.child_nodes:
                cle: bytes = child.data.tobytes()
                if cle not in visites:
                    visites.add(cle)
                    frontiere.append(child)

        self._execute_time = timer() - start
        self._number_state_explore = iteration
        return None