import numpy as np
from Cell import Cell

class MinesweeperBoard:
    def __init__(self, rows:int, cols:int, numMines: int) -> None:

        self.rows: int = rows
        self.cols:int = cols
        self.numMines:int = numMines
        self.isFinished = False

        # the board object
        self.theBoard: np.ndarray = self.makeGrid()


    """
    create a 2d array of cells with dimensions = (rows x cols)
    make the first numMines bombs; rest non-bombs
    randomly shuffle array
    return grid
    """
    def makeGrid(self) -> np.ndarray:
        raise NotImplementedError

    """
    takes a coordinate and reveals the cell; modifies self.theBoard
    will call cascadeCell if number == 0
    returns bool for finished or not
    """
    def revealCell(self, row:int, col:int) -> bool:
        raise NotImplementedError

    """
    calculates a cell's number based on its neighbors
    sets the cell's property
    """
    def calcAdjacentBombs(self, row:int, col:int) -> None:
        raise NotImplementedError

    """
    returns a list of cell objects that neighbor a cell
    handles OOB cases
    used for cascading and calculating cell number
    """
    def getNeighborCells(self, cell:Cell) -> list[Cell]:
        raise NotImplementedError

    """
    called on a cell when its number == 0
    used to determine the size of this cascade
    if reveal is True, will reveal the cells
    returns the size of cascade
    """
    def cascade(self, cell:Cell, reveal:bool) -> int:
        raise NotImplementedError

    # test