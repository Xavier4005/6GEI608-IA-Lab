#Xavier
from pathlib import Path
from multiprocessing import Process, Queue
from queue import Empty
from PuzzleNode import PuzzleNode
from PuzzleTree import PuzzleTree
from SeekAlgorithm import SeekAlgorithm
from IO import IO
from BFS import BFS
from DFS import DFS
from IDF import IDF
import numpy as np

DOSSIER_INPUTS = Path(__file__).parent.parent / "input-Ex1"
DOSSIER_RESULTATS = Path(__file__).parent / "resultats"
OBJECTIF = np.array([[1,2,3],[4,5,6],[7,8,0]], dtype=np.int32)
ALGORITHMES: dict[str, type[SeekAlgorithm]] = {"BFS": BFS, "DFS": DFS, "IDF": IDF}
DELAI_MAX = 60


def nombre_inversions(grille) -> int:
    valeurs = [int(v) for v in grille.flatten() if v != 0]
    return sum(1 for i in range(len(valeurs)) for j in range(i + 1, len(valeurs)) if valeurs[i] > valeurs[j])


def est_soluble(grille, objectif) -> bool:
    return nombre_inversions(grille) % 2 == nombre_inversions(objectif) % 2


def executer(nom: str, fichier: Path, file_resultats: Queue) -> None:
    grille = IO.read_file(fichier)
    zero_row, zero_col = np.argwhere(grille == 0)[0]
    node = PuzzleNode(grille, (int(zero_row), int(zero_col)), None)

    algo = ALGORITHMES[nom]()
    subnode : PuzzleNode | None = algo.seek(PuzzleTree(node), OBJECTIF)

    if subnode is None:
        file_resultats.put(None)
        return

    chemin = []
    n = subnode
    while n is not None:
        chemin.append(n.data)
        n = n.parent_node
    chemin.reverse()

    IO.write_file(DOSSIER_RESULTATS / f"{fichier.stem}_{nom}.txt", chemin)
    file_resultats.put((len(chemin) - 1, algo._number_state_explore, algo._execute_time))


def main():
    print("Hello from algorithmesrecherche1!")

    fichiers = sorted(DOSSIER_INPUTS.glob("*.txt"))
    if len(fichiers) == 0:
        print(f"Aucun fichier .txt trouvé dans {DOSSIER_INPUTS}")
        return

    print(f"\n{'Fichier':<12}{'Algo':<6}{'Coups':>8}{'États':>10}{'Temps (s)':>11}")
    for fichier in fichiers:
        grille = IO.read_file(fichier)

        if not est_soluble(grille, OBJECTIF):
            print(f"{fichier.name:<12}{'-':<6}  insoluble, aucun algorithme lancé")
            continue

        for nom in ALGORITHMES:
            file_resultats = Queue()
            processus = Process(target=executer, args=(nom, fichier, file_resultats))
            processus.start()
            processus.join(DELAI_MAX)

            if processus.is_alive():
                processus.terminate()
                processus.join()
                print(f"{fichier.name:<12}{nom:<6}  arrêté après {DELAI_MAX} s")
                continue

            try:
                resultat = file_resultats.get(timeout=1)
            except Empty:
                print(f"{fichier.name:<12}{nom:<6}  échec (erreur ou mémoire insuffisante)")
                continue

            if resultat is None:
                print(f"{fichier.name:<12}{nom:<6}  aucune solution trouvée")
                continue

            coups, etats, temps = resultat
            print(f"{fichier.name:<12}{nom:<6}{coups:>8}{etats:>10}{temps:>11.3f}")


if __name__ == "__main__":
    main()