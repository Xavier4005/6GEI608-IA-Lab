from puzzleNode import PuzzleNode
import array

class PuzzleNode:
    _data : array[int,int]
    _parent_node : PuzzleNode
    _zero_position : tuple[int,int]
    _child_nodes : list[PuzzleNode]

    def __init__(self, data : array[int,int], zero_position : tuple[int,int], parent_node : PuzzleNode):
        self._data = data
        self._zero_position = zero_position
        self._parent_node = parent_node
        self._child_nodes = list()

    @property
    def data(self) -> array[int,int]:
        return self._data

    @property
    def zero_position(self) -> tuple[int,int]:
        return self._zero_position

    @property
    def parent_node(self) -> PuzzleNode:
        return self._parent_node

    @property
    def child_nodes(self) -> list[PuzzleNode]:
        return self._child_nodes
