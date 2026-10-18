#Eliel

from SeekAlgorithm import SeekAlgorithm
from PuzzleTree import PuzzleTree
from PuzzleNode import PuzzleNode
from timeit import default_timer as timer
from itertools import count
import numpy.typing as npt
import numpy as np
import heapq


class AStar(SeekAlgorithm):

    def seek(self, tree: PuzzleTree, objectif: npt.NDArray[np.int32]) -> PuzzleNode | None:
        iteration: int = 0
        start: float = timer()
        compteur = count()

        frontiere: list[tuple[int, int, int, PuzzleNode]] = []
        heapq.heappush(frontiere, (self.heuristique(tree.root, objectif), next(compteur), 0, tree.root))

        visites: set[bytes] = set()

        while len(frontiere) != 0:
            _, _, g, actual_node = heapq.heappop(frontiere)

            cle: bytes = actual_node.data.tobytes()
            if cle in visites:
                continue
            visites.add(cle)

            self._iteration_frontiere.append((iteration, len(frontiere)))
            iteration += 1

            if self.verify(actual_node, objectif):
                self._execute_time = timer() - start
                self._number_state_explore = iteration
                return actual_node

            self.explore(actual_node)
            for child in actual_node.child_nodes:
                if child.data.tobytes() not in visites:
                    g_child: int = g + 1
                    f_child: int = g_child + self.heuristique(child, objectif)
                    heapq.heappush(frontiere, (f_child, next(compteur), g_child, child))

        self._execute_time = timer() - start
        self._number_state_explore = iteration
        return None

    def heuristique(self, node: PuzzleNode, objectif: npt.NDArray[np.int32]) -> int:
        h1: int = int(np.count_nonzero((node.data != 0) & (node.data != objectif)))

        h2: int = 0
        for valeur in range(1, node.data.size):
            ligne, col = np.argwhere(node.data == valeur)[0]
            ligne_obj, col_obj = np.argwhere(objectif == valeur)[0]
            h2 += abs(int(ligne) - int(ligne_obj)) + abs(int(col) - int(col_obj))

        return max(h1, h2)