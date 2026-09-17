#Xavier
from puzzleNode import PuzzleNode
from puzzleTree import PuzzleTree
from idf import IDF
import numpy as np


def main():
    print("Hello from algorithmesrecherche1!")

    node = PuzzleNode(np.array([[7,2,4],[5,0,6],[8,3,1]]), (1,1), None)

    idf = IDF()
    subnode : PuzzleNode | None = idf.seek(PuzzleTree(node), np.array([[1,2,3],[4,5,6],[7,8,0]]))

    if subnode is None:
        print("Aucun résultat")
    else:
        print(subnode.data)



if __name__ == "__main__":
    main()
