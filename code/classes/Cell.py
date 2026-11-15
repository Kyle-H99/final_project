
class Cell:
    def __init__(self, isBomb:bool, row:int, col:int) -> None:

        self.isBomb:bool = isBomb
        self.revealed:bool = False

        self.adjacentBombs:int # to be filled when board is made
        self.row:int = row
        self.col:int = col


    def setNumber(self, num:int) -> None:
        self.adjacentBombs = num


    def __str__(self) -> str:
        if self.revealed:
            return f" {self.adjacentBombs} "
        else:
            return f" -1 "