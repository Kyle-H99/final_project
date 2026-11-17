import numpy as np
from .Cell import Cell

class MinesweeperBoard:

    def __init__(self, rows:int, cols:int, mines: int, seed:int | None) -> None:

        self.rows: int = rows
        self.cols:int = cols
        self.mines:int = mines
        self.seed:int | None = seed

        # the board objects, all arrays hold Cells
        self.bombs: np.ndarray = self._makeBombs(mines)
        self.safeCells: np.ndarray = self._makeSafeCells(rows * cols - mines)
        self.theBoard: np.ndarray = self._makeGrid(self.bombs, self.safeCells)
        self._assignNumbersToCells()


############ creation methods
    def _makeBombs(self, num:int) -> np.ndarray:
        return np.array([Cell(isBomb=True) for _ in range(num)])

    def _makeSafeCells(self, num:int) -> np.ndarray:
        return np.array([Cell(isBomb=False) for _ in range(num)])


    def _makeGrid(self, bombs: np.ndarray, safeCells:np.ndarray) -> np.ndarray:
        """
        - combine all bombs and non-bombs
        - reshape into 2d array
        - randomly shuffle array with seed
        - return grid
        """
        flatGrid: np.ndarray = np.concatenate([bombs, safeCells])

        rng = np.random.default_rng(seed=self.seed)
        rng.shuffle(flatGrid)

        # reshape
        reshapedGrid: np.ndarray = flatGrid.reshape(self.rows, self.cols)
        for row in range(self.rows):
            for col in range(self.cols):
                reshapedGrid[row][col].setCoords(row, col)

        return reshapedGrid
    
    """
    calculates a cell's number based on its neighbors
    sets the cell's property
    """
    def _calcAdjacentBombs(self, cell:Cell) -> None:

        neighbors:list[Cell] = self.getNeighborCells(cell)

        count:int = 0

        for neighbor in neighbors:
            if neighbor.isBomb:
                count += 1

        cell.adjacentBombs = count

    """
    """
    def _assignNumbersToCells(self) -> None:
        for i in self.theBoard.flatten():
            self._calcAdjacentBombs(i)
############



# getters

    """
    returns bool for board being finished
    """
    def isFinished(self) -> bool:
        for cell in self.safeCells:
            if not cell.revealed:
                return False

        return True
        
    """
    returns a list of cell objects that neighbor a cell
    handles OOB cases
    used for cascading and calculating cell number
    """
    def getNeighborCells(self, cell:Cell) -> list[Cell]:

        # calc offsets
        offsets: np.ndarray = np.array([[i,j] for i in range(-1,2) for j in range(-1,2) if [i,j] != [0,0]])

        # add them to our cell's coords to get neighbor coords
        neighborCoords: np.ndarray = np.array([cell.row, cell.col]) + offsets

        # create a mask for coords in range, filter out rest
        rows = neighborCoords[:,0]
        cols = neighborCoords[:,1]

        coordsInRange: np.ndarray = (rows >= 0) & (rows < self.rows) & (cols >= 0) & (cols < self.cols)
        filteredCoords:np.ndarray = neighborCoords[coordsInRange]

        neighbors:list[Cell] = [self.theBoard[r,c] for r, c in filteredCoords] #type: ignore

        return neighbors

    """
    pretty print the board
    """
    def showRevealedBoard(self) -> None:
        print()
        for row in range(self.rows):
            for col in range(self.cols):
                print(self.theBoard[row][col].showTrueVal(), end= " ")
            print()



# setters

    """
    takes a coordinate and reveals the cell; modifies self.theBoard
    will call cascadeCell if number == 0

    throws if reveal called on revealed cell
    """
    def revealCell(self, row:int, col:int) -> None:
        theCell:Cell = self.theBoard[row][col]

        if theCell.adjacentBombs == 0:
            self.cascade(theCell, True)
        else:
            theCell.reveal()


    """
    called on a cell when its number == 0
    if reveal is True, will reveal the cells
    returns the list of cells in the cascade
    """
    def cascade(self, cell:Cell, reveal:bool) -> list[Cell]:

        cells: list[Cell] = self._cascadeHelper(cell, reveal)

        # reset visits
        for cell in self.safeCells.flatten():
            cell.visited = False

        return cells


    """
    base case: cell is visited already, or is not a 0 cell
    recursive case: 
        - mark cell visited

    """
    def _cascadeHelper(self, cell:Cell, reveal:bool) -> list[Cell]:

        if cell.visited or cell.isBomb or cell.adjacentBombs > 0:
            return []

        thisCascade: list[Cell] = []

        cell.visited = True

        for neighbor in self.getNeighborCells(cell):
            thisCascade.extend(self._cascadeHelper(neighbor, reveal))

        if reveal:
            cell.reveal()

        thisCascade.append(cell)

        return thisCascade



    """
    finds a longest cascade. doesn't break ties, chooses first one with max
    used for first turn so as to reduce initial guessing
    if no cascade exists, i.e. no 0 cells, list is empty
    """
    def findLongestCascade(self) -> list[Cell]:

        longestCascade: list[Cell] = []

        for cell in self.safeCells.flatten():
            if cell.adjacentBombs == 0:
                cells: list[Cell] = self.cascade(cell, reveal=False)
                if len(cells) > len(longestCascade):
                    longestCascade = cells

        return longestCascade


