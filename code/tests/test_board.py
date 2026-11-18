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
        self.assertEqual(self.board_10_10.remainingSafeCells, 80)

        # test for dupes
        self.assertEqual(len(set(self.board_10_10.safeCells)), 80)
        self.assertEqual(len(set(self.board_10_10.bombs)), 20)

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

        self.assertEqual(set(neighbors), set([right, down, diag]))


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
        self.board_10_10.showBoard(trueVals=True)


    """
    test various cascades on the board
    """
    def test_cascade_1(self):
        
        start:Cell = self.theBoard[0][0]
        cascade: list[Cell] = self.board_10_10.cascade(start, reveal=False)
        self.assertEqual(len(cascade), 7)

        compare: list[Cell] = []
        compare.extend([self.theBoard[i][j] for i in range(2) for j in range(3)])
        compare.append(self.theBoard[2][0])

        self.assertEqual(set(compare), set(cascade))

    def test_cascade_2(self):

        start:Cell = self.theBoard[0][6]
        cascade: list[Cell] = self.board_10_10.cascade(start, reveal=False)
        self.assertEqual(len(cascade), 12)

        cells: list[Cell] = []

        cells.extend([self.theBoard[row][col] for row in range(4) for col in range(6,8)])
        cells.extend([self.theBoard[row][col] for row in range(4,6) for col in range(8,10)])

        self.assertEqual(set(cells), set(cascade))

    def test_cascade_3(self):

        start:Cell = self.theBoard[6][0]
        cascade: list[Cell] = self.board_10_10.cascade(start, reveal=False)
        self.assertEqual(len(cascade), 1)
        self.assertEqual(cascade[0], start)

    def test_longestCascade(self):

        cascade: list[Cell] = self.board_10_10.findLongestCascade()
        cells: list[Cell] = []

        cells.extend([self.theBoard[row][col] for row in range(4) for col in range(6,8)])
        cells.extend([self.theBoard[row][col] for row in range(4,6) for col in range(8,10)])

        self.assertEqual(set(cells), set(cascade))
        self.assertEqual(len(cascade), 12)


    """
    add tests for revealing and finished games
    """
    def test_reveal_cascade(self):

        self.board_10_10.revealCell(0,0)
        self.assertFalse(self.board_10_10.isFinished())
        self.assertEqual(self.board_10_10.remainingSafeCells, 80-7)

    def test_reveal_bomb(self):

        self.board_10_10.revealCell(1, 4)
        self.assertTrue(self.board_10_10.isFinished())
        self.assertTrue(self.theBoard[1][4].revealed)


    def test_reveal_win(self):

        for cell in self.board_10_10.safeCells:
            if not cell.revealed:
                self.board_10_10.revealCell(cell.row, cell.col)

        self.assertTrue(self.board_10_10.isFinished())


    
if __name__ == "__main__":
    unittest.main()
