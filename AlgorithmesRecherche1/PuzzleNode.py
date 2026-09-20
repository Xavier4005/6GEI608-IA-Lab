import numpy as np
import numpy.typing as npt
from typing import Self


class PuzzleNode:
    _data : npt.NDArray[np.int32]
    _parent_node : Self | None
    _zero_position : tuple[int,int]
    _child_nodes : list[Self]

    def __init__(self, data : npt.NDArray[np.int32], zero_position : tuple[int,int] | None = None ,parent_node : Self | None = None):
        self._data = data
        self._child_nodes = list()
        self._parent_node = parent_node

        if zero_position is None:
            coords = np.where(data == 0)
            if len(coords[0] > 0):
                self._zero_position = (coords[0][0], coords[1][0])
            else:
                self._zero_position = (0,0)
        else:
            self._zero_position = zero_position

    @property
    def data(self) -> npt.NDArray[np.int32]:
        return self._data

    @property
    def zero_position(self) -> tuple[int,int]:
        return self._zero_position

    @property
    def parent_node(self) -> Self | None:
        return self._parent_node

    @property
    def child_nodes(self) -> list[Self]:
        return self._child_nodes
