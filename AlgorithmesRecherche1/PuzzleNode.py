from puzzleNode import PuzzleNode

class PuzzleNode:
    _parent_node : PuzzleNode

    def __init__(self, data, zero_position, parent_node):
        self._data = data
        self._zero_position = zero_position
        self._parent_node = parent_node
        self._child_nodes = list()

    @property
    def data(self):
        return self._data

    @property
    def zero_position(self):
        return self._zero_position

    @property
    def parent_node(self):
        return self._parent_node

    @property
    def child_nodes(self):
        return self._child_nodes
