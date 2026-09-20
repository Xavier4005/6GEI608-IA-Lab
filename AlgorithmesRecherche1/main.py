# Xavier

import sys
from pathlib import Path
from puzzleNode import PuzzleNode
from puzzleTree import PuzzleTree
from seekAlgorithm import SeekAlgorithm
from IO import IO
from bfs import BFS
from dfs import DFS
from idf import IDF
import numpy.typing as npt
import numpy as np


DOSSIER_PROJET = Path(__file__).parent
DOSSIER_INPUTS = DOSSIER_PROJET.parent / "input-Ex1"
DOSSIER_RESULTATS = DOSSIER_PROJET / "resultats"

OBJECTIF = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
], dtype=np.int32)

ALGORITHMES: dict[str, type[SeekAlgorithm]] = {
    "BFS": BFS,
    "DFS": DFS,
    "IDF": IDF
}

NOMBRE_EXECUTIONS = 10


def main():


    if len(sys.argv) > 1:
        fichiers = [
            Path(argument)
            for argument in sys.argv[1:]
        ]
    else:
        fichiers = sorted(
            DOSSIER_INPUTS.glob("*.txt")
        )

    if len(fichiers) == 0:
        print(
            f"Aucun fichier .txt trouvé dans {DOSSIER_INPUTS}"
        )
        return

    for fichier in fichiers:
        algo_type: type[SeekAlgorithm]
        for algo_type in ALGORITHMES.values():
            i : int = 0
            for i in range(NOMBRE_EXECUTIONS):
                algo : SeekAlgorithm = algo_type()
                initial_state : npt.NDArray[np.int32] = IO.read_file(fichier.absolute())
                tree : PuzzleTree = PuzzleTree(PuzzleNode(initial_state))
                algo.seek(tree, OBJECTIF)
                IO.write_file(DOSSIER_RESULTATS / fichier.stem / ("Resultat" + algo_type.__name__) / (str(i+1) + ".txt"), algo._iteration_frontiere, algo._number_state_explore, algo._execute_time)


if __name__ == "__main__":
    main()