# Xavier

import sys
from pathlib import Path
from PuzzleNode import PuzzleNode
from puzzleTree import PuzzleTree
from SeekAlgorithm import SeekAlgorithm
from IO import IO
from BFS import BFS
from DFS import DFS
from IDF import IDF
import numpy.typing as npt
import numpy as np


DOSSIER_PROJET = Path(__file__).parent
DOSSIER_INPUTS = DOSSIER_PROJET.parent / "input-Ex1"
DOSSIER_RESULTATS = DOSSIER_PROJET / "resultats"

ACTIONS = {
    (-1, 0): "haut",
    (1, 0): "bas",
    (0, -1): "gauche",
    (0, 1): "droite"
}

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

def chemin_actions(node: PuzzleNode) -> list[str]:
    actions: list[str] = []

    while node.parent_node is not None:
        parent: PuzzleNode = node.parent_node

        deplacement = (
            node.zero_position[0] - parent.zero_position[0],
            node.zero_position[1] - parent.zero_position[1]
        )

        actions.append(ACTIONS[deplacement])
        node = parent

    actions.reverse()

    return actions


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
            action : list[str] = list[str]()
            for i in range(NOMBRE_EXECUTIONS):
                algo : SeekAlgorithm = algo_type()
                initial_state : npt.NDArray[np.int32] = IO.read_file(fichier.absolute())
                tree : PuzzleTree = PuzzleTree(PuzzleNode(initial_state))
                responce_node : PuzzleNode = algo.seek(tree, OBJECTIF)
                if responce_node is not None:
                    print("Resultat " + fichier.stem + " " + algo_type.__name__ + " essai " + str(i+1) + " Réussi")
                    action = chemin_actions(responce_node)
                    IO.write_file(DOSSIER_RESULTATS / fichier.stem / ("Resultat" + algo_type.__name__) / (str(i+1) + ".txt"), algo._iteration_frontiere, algo._number_state_explore, algo._execute_time)
                else :
                    print("Resultat " + fichier.stem + " " + algo_type.__name__ + " essai " + str(i+1) + " Imposible")
            if len(action) != 0:
                print("Résolution : " + " ".join(action))


if __name__ == "__main__":
    main()