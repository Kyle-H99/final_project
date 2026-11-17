import unittest 
from classes.Board import *
from classes.Cell import *

class TestBoard(unittest.TestCase):
    def setUp(self) -> None:
        self.board_10_10 = MinesweeperBoard(rows=10, cols=10, mines=20, seed=1234)
        self.theBoard = self.board_10_10.theBoard


    def test_init(self):
        self.assertEqual(self.theBoard.shape, (10,10))
        self.assertEqual(self.board_10_10.bombs.size, 20)
        self.assertEqual(self.board_10_10.safeCells.size, 80)

        for cell in self.board_10_10.safeCells:
            self.assertFalse(cell.isBomb)

        for cell in self.board_10_10.bombs:
            self.assertTrue(cell.isBomb)

    def test_getNeighbors_0_0(self):
        cell:Cell = self.theBoard[0][0]
        neighbors: list[Cell] = self.board_10_10.getNeighborCells(cell)

        self.assertEqual(len(neighbors),3)

        right:Cell = self.theBoard[0][1]
        down:Cell = self.theBoard[1][0]
        diag:Cell = self.theBoard[1][1]

        self.assertTrue(right in neighbors)
        self.assertTrue(down in neighbors)
        self.assertTrue(diag in neighbors)

    def test_getNeighbors_interior(self):
        
        cell: Cell = self.theBoard[5][5]
        neighbors: list[Cell] = self.board_10_10.getNeighborCells(cell)

        self.assertEqual(len(neighbors), 8)

        expected: list[Cell] = [
            self.theBoard[4][4], self.theBoard[4][5], self.theBoard[4][6],
            self.theBoard[5][4],                      self.theBoard[5][6],
            self.theBoard[6][4], self.theBoard[6][5], self.theBoard[6][6],
        ]

        for n in expected:
            self.assertTrue(n in neighbors)

        # the cell itself must not be counted as its own neighbor
        self.assertFalse(cell in neighbors)

        # no duplicates: 8 distinct objects
        self.assertEqual(len({id(n) for n in neighbors}), 8)

    """
    visually inspect that numbers are calculated correctly
    """
    def test_print(self):
        self.board_10_10.showRevealedBoard()

    """
    test a cascade, seed=1234, 10x10, 20 mines
    """

    """
    test various cascades on the board
    """
    def test_cascade_count(self):
        start:Cell = self.theBoard[0][0]
        cascade: list[Cell] = self.board_10_10.cascade(start, reveal=False)
        self.assertEqual(len(cascade), 7)

        start:Cell = self.theBoard[0][6]
        cascade: list[Cell] = self.board_10_10.cascade(start, reveal=False)
        self.assertEqual(len(cascade), 12)

        start:Cell = self.theBoard[6][0]
        cascade: list[Cell] = self.board_10_10.cascade(start, reveal=False)
        self.assertEqual(len(cascade), 1)
        self.assertEqual(cascade[0], start)

        start:Cell = self.theBoard[6][0]
        cascade: list[Cell] = self.board_10_10.cascade(start, reveal=True)
        self.assertTrue(start.revealed, True)


    def test_longestCascade(self):

        cascade: list[Cell] = self.board_10_10.findLongestCascade()
        cells: list[Cell] = []

        cells.extend([self.theBoard[row][col] for row in range(4) for col in range(6,8)])
        cells.extend([self.theBoard[row][col] for row in range(4,6) for col in range(8,10)])

        self.assertEqual(set(cells), set(cascade))
        self.assertEqual(len(cascade), 12)

    
if __name__ == "__main__":
    unittest.main()
