
class Cell:
    def __init__(self, isBomb:bool) -> None:

        self.isBomb:bool = isBomb
        self.revealed:bool = False
        self.visited = False

        self.adjacentBombs:int # to be filled when board is made
        self.row:int
        self.col:int


    def setNumber(self, num:int) -> None:
        self.adjacentBombs = num

    def reveal(self) -> None:
        if self.revealed:
            raise Exception("reveal called on revealed cell", self)

        self.revealed = True

    def hide(self) -> None:
        if not self.revealed:
            raise Exception("reveal called on revealed cell", self)

        self.revealed = False

    def setCoords(self, row:int, col:int) -> None:
        self.row, self.col = row, col

    def getTrueVal(self) -> str:
        if self.isBomb:
            return "B"
        return f"{self.adjacentBombs}"

    def getCurrentVal(self) -> str:
        if not self.revealed:
            return "-1"
        return self.getTrueVal()