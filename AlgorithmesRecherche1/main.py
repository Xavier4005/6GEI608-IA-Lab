#Xavier
from puzzleNode import PuzzleNode
from idf import IDF
import numpy as np


def main():
    print("Hello from algorithmesrecherche1!")

    node = PuzzleNode(np.array([[7,2,4],[5,0,6],[8,3,1]]), (1,1), None)

    idf = IDF()
    idf.explore(node)

    subnode : PuzzleNode

    for subnode in node.child_nodes:
        print(subnode.data)

    print(node)



if __name__ == "__main__":
    main()
