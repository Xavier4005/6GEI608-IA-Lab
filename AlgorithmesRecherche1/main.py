# Xavier

import sys
from pathlib import Path
from PuzzleNode import PuzzleNode
from PuzzleTree import PuzzleTree
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

ACTIONS = {
    (-1, 0): "haut",
    (1, 0): "bas",
    (0, -1): "gauche",
    (0, 1): "droite"
}


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


def executer_une_fois(
    Algo: type[SeekAlgorithm],
    grille: npt.NDArray[np.int32]
) -> tuple[list[str] | None, list[tuple[int, int]], int, float]:

    zero_row, zero_col = np.argwhere(grille == 0)[0]

    node = PuzzleNode(
        grille.copy(),
        (int(zero_row), int(zero_col)),
        None
    )

    algo: SeekAlgorithm = Algo()

    subnode: PuzzleNode | None = algo.seek(
        PuzzleTree(node),
        OBJECTIF
    )

    temps_execution: float = algo._execute_time
    tailles_frontiere: list[tuple[int, int]] = algo._iteration_frontiere
    nombre_etats: int = algo._number_state_explore

    actions = chemin_actions(subnode) if subnode is not None else None

    return actions, tailles_frontiere, nombre_etats, temps_execution


def resoudre(fichier: Path) -> None:

    print(f"\n===== {fichier.name} =====")

    grille = IO.read_file(fichier)

    print(grille)

    for nom, Algo in ALGORITHMES.items():

        print(f"\n{nom}")

        actions = None

        for execution in range(1, NOMBRE_EXECUTIONS + 1):

            actions, tailles_frontiere, nombre_etats, temps_execution = executer_une_fois(
                Algo,
                grille
            )

            fichier_statistiques = IO.export_statistiques(
                DOSSIER_RESULTATS,
                fichier.stem,
                nom,
                execution,
                tailles_frontiere,
                nombre_etats,
                temps_execution
            )

            print(
                f"  exécution {execution:2d} : "
                f"{nombre_etats} états explorés, "
                f"{temps_execution:.3f} s -> "
                f"{fichier_statistiques.relative_to(DOSSIER_PROJET)}"
            )

        if actions is None:
            print("  Aucune solution : l'état objectif n'est pas atteignable")
            continue

        dossier = DOSSIER_RESULTATS / fichier.stem / nom
        fichier_solution = dossier / "solution.txt"

        IO.write_solution(
            fichier_solution,
            actions
        )

        if len(actions) <= 40:
            print(
                f"  Solution en {len(actions)} actions : "
                f"{', '.join(actions)}"
            )
        else:
            print(
                f"  Solution en {len(actions)} actions -> "
                f"{fichier_solution.relative_to(DOSSIER_PROJET)}"
            )


def main():

    print("Hello from algorithmesrecherche1!")

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
        resoudre(fichier)


if __name__ == "__main__":
    main()