import numpy as np
from .Cell import Cell

class MinesweeperBoard:

    def __init__(self, rows:int, cols:int, mines: int, seed:int | None) -> None:

        self.rows: int = rows
        self.cols:int = cols
        self.mines:int = mines
        self.seed:int | None = seed

        # the board objects, all arrays hold Cells
        self.bombs: np.ndarray = self._makeBombs(num=mines)
        self.safeCells: np.ndarray = self._makeSafeCells(num=rows * cols - mines)
        self.theBoard: np.ndarray = self._makeGrid(bombs=self.bombs, safeCells=self.safeCells, rows=rows, cols=cols)
        self._assignNumbersToCells()

        # properties for gameplay
        self.remainingSafeCells:int = len(self.safeCells)


# creation methods
    def _makeBombs(self, num:int) -> np.ndarray:
        return np.array([Cell(isBomb=True) for _ in range(num)])

    def _makeSafeCells(self, num:int) -> np.ndarray:
        return np.array([Cell(isBomb=False) for _ in range(num)])

    def _makeGrid(self, bombs: np.ndarray, safeCells:np.ndarray, rows:int, cols:int) -> np.ndarray:
        """
        - combine all bombs and non-bombs
        - reshape into 2d array
        - randomly shuffle array with seed
        - return grid
        """
        flatGrid: np.ndarray = np.concatenate([bombs, safeCells])

        rng = np.random.default_rng(seed=self.seed)
        rng.shuffle(flatGrid)

        # cheeky method for assigning coords
        for i, cell in enumerate(flatGrid):
            cell.setCoords(*divmod(i, cols))

        return flatGrid.reshape(rows, cols)
    
    def _calcAdjacentBombs(self, cell:Cell) -> None:
        """
        - calculates a cell's number based on its neighbors
        - updates the cell object
        """

        neighbors:list[Cell] = self.getNeighborCells(cell)

        cell.adjacentBombs = sum(neighbor.isBomb for neighbor in neighbors)

    def _assignNumbersToCells(self) -> None:
        """
        calculates each cell's adjacent bombs
        """
        for i in self.theBoard.flatten():
            self._calcAdjacentBombs(i)


# getters

    
    def isFinished(self) -> bool:
        """
        returns bool for board being finished
        """
        return (
            any(cell.revealed for cell in self.bombs)  # a bomb was revealed (loss)
            or self.remainingSafeCells == 0            # all safe cells revealed (win)
        )
        
    def getNeighborCells(self, cell:Cell) -> list[Cell]:
        """
        - returns a list of cell objects that neighbor a cell
        - handles OOB cases
        - used for cascading and calculating cell number
        """

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

    def getCurrentBoard(self, trueVals:bool) -> list[list[int]]:
        """
        - returns the 2d representation of the board
        - called by encode()
        - bombs should never be encoded, so error will raise error if that happens
        """
        try:
            values: list[list[int]] = [[int(cell.getCurrentVal()) for cell in row] for row in self.theBoard]
        except ValueError as e:
            raise ValueError(f"getCurrentBoard() called with bomb revealed. Game should be over", e)

        return values


    def getTrueBoard(self) -> list[list[str]]:
        """
        - Returns board with true values
        - used for testing; make sure board is being generated properly
        """
        return [[cell.getTrueVal() for cell in row] for row in self.theBoard] 
    

    def prettyPrintBoard(self, trueVals:bool) -> None:

        print()
        for row in range(self.rows):
            for col in range(self.cols):
                cell:Cell = self.theBoard[row][col]
                val = cell.getTrueVal() if trueVals else cell.getCurrentVal()
                print(f"{val:>2}", end=" ")
            print()


    def findLongestCascade(self) -> list[Cell]:
        """
        - finds a longest cascade, doesn't break ties
        - used for first turn so as to reduce initial guessing
        - if no cascade exists, i.e. no 0 cells, list is empty
        """
        longestCascade: list[Cell] = []

        for cell in self.safeCells.flatten():
            if cell.adjacentBombs == 0:
                cells: list[Cell] = self.cascade(cell, reveal=False)
                if len(cells) > len(longestCascade):
                    longestCascade = cells

        return longestCascade

    def getEncoding(self) -> np.ndarray:
        """
        - encodes the grid to a 10 x Rows x Cols array
        - input into the CNN
        - first dimension represents the channel for a 2D one hot encoding for cells of that value. next two dimensions are the encoding
        - channels 0-8 represent channels for cells of that number
        - channel 9 is unknown cells
        - see scrap notebook for how this works. Used claude to help
        - Note: this will be called after an action is taken and the game is deemed not finished, so we should never encode bombs.
        """

        board: np.ndarray = np.array(self.getCurrentBoard(trueVals=False))
        board = np.where(board == -1, 9, board) # recode -1 to 9

        # see scrap notebook
        eye: np.ndarray = np.eye(10, dtype=np.float32)[board]
        eye = np.moveaxis(eye, -1, 0)

        return eye


# setters


    def revealCell(self, row:int, col:int) -> None:
        """
        - takes a coordinate and reveals the cell; modifies self.theBoard
        - will call cascadeCell if number == 0
        - throws if reveal called on revealed cell
        """

        theCell:Cell = self.theBoard[row][col]
        if theCell.isBomb:
            theCell.reveal()
            return

        if theCell.adjacentBombs > 0:
            self.remainingSafeCells -= 1
            theCell.reveal()
        else:
            cascade: list[Cell] = self.cascade(theCell, True)
            self.remainingSafeCells -= len(cascade)

    def cascade(self, cell:Cell, reveal:bool) -> list[Cell]:
        """
        - called on a cell when its number == 0
        - if reveal is True, will reveal the cells
        - returns the list of cells in the cascade
        """
        
        cells: list[Cell] = self._cascadeHelper(cell, reveal)

        # reset visits
        for cell in self.safeCells.flatten():
            cell.visited = False

        return cells

    def _cascadeHelper(self, cell:Cell, reveal:bool) -> list[Cell]:
        """
        base case
            - cell is visited already, or is not a 0 cell
        recursive case: 
            - mark cell as visited
            - get a list of all upstream cells
            - add this cell to it and return list
        """
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

