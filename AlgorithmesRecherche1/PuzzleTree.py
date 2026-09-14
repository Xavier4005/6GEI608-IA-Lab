from puzzleNode import PuzzleNode

class PuzzleTree :
    _root : PuzzleNode

    def __init__(self, root : PuzzleNode):
        self._root = root

    @property
    def root(self):
        return self._root