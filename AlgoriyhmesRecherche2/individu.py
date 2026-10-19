import numpy as np
import numpy.typing as npt

class Individu:
        sudoku: npt.NDArray[np.int32]
        fitness: int

        def __init__(self, sudoku : npt.NDArray[np.int32], fitness : int):
                self.sudoku = sudoku
                self.fitness = fitness