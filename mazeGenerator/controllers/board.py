"""
File: board.py
Date Created: 19/11/22
"""
from mazeGenerator.config import Config
from mazeGenerator.models import Tile, Cell
from mazeGenerator.response import Response, Ok, Err
from mazeGenerator.response import ExceedsBounds, EmptyBoard

from typing import List


class Board:
    def __init__(self):
        self.__config: Config = Config()
        self.height: int = 0  # Width
        self.width: int = 0
        self.tileSet: List[Tile] = []
        self.board: List[Cell] = []
        self.collapsed = False

    def setWidth(self, widthInput: int) -> Response:
        if not isinstance(widthInput, int):
            return Err(TypeError)

        if widthInput > self.__config.get("maxWidth"):
            return Err(ExceedsBounds)

        self.width = widthInput
        return Ok(self.width)

    def setHeight(self, heightInput: int) -> Response:
        if not isinstance(heightInput, int):
            return Err(TypeError)

        if heightInput > self.__config.get("maxHeight"):
            return Err(ExceedsBounds)   

        self.height = heightInput
        return Ok(self.height)

    def getIdx(self, row: int, col: int) -> Response:
        if row > self.height or col > self.width or row < 0 or col < 0:
            return Err(ExceedsBounds)

        idx = (row * self.width + col)
        return Ok(idx)

    def getNeighbours(self, row: int, col: int) -> List[Cell]:
        neighbours: List[Cell] = []
        for delta_row in [-1, 0, 1]:
            for delta_col in [-1, 0, 1]:
                if (delta_row, delta_col) in [(-1, -1), (1, -1), (-1, 1), (1, 1), (0, 0)]:  # Remove corners and centre
                    # There probably was a better way of doing this then force skipping half the generated parameters
                    continue

                neighbour_row = (row + delta_row) % self.height
                neighbour_col = (col + delta_col) % self.width
                idx = self.getIdx(neighbour_row, neighbour_col)
                if idx.success:
                    neighbours.append(self.board[idx.data])

        return neighbours

    def generateBoard(self):
        for row in range(self.height):
            for col in range(self.width):
                self.board.append(Cell(self.tileSet, row=row, col=col))

    def findLowestEntropy(self) -> Response:
        if len(self.board) == 0:
            return Err(EmptyBoard)
        lowestEntropy = self.board[0]
        for cell in self.board:
            if cell.entropy < lowestEntropy.entropy:
                lowestEntropy = cell

        return Ok(lowestEntropy)

    def performCollapse(self):
        invalid = False
        print("hiyaa?", self.board)
        while not invalid and not self.collapsed:
            invalid = self.calculateEntropy()
            if self.stateComplete():
                self.collapsed = True

            lowestCell = self.findLowestEntropy()
            if lowestCell.success:
                res = lowestCell.data.collapse()

        print(invalid, self.collapsed, self.board)
        e = self.board[0].getEdge("pos-x")
        print(e)
        for tile in self.tileSet:
            if tile.getEdge("neg-x") == e:
                print(tile)

    @staticmethod
    def reverse_direction(direction):
        flip = {"pos": "neg", "neg": "pos"}
        direction = direction.split("-")
        direction[0] = flip[direction[0]]
        return "-".join(direction)

    def calculateEntropy(self):
        invalidState = False
        idx = 0
        while not invalidState and idx < len(self.board):
            cell = self.board[idx]
            if cell.collapsed:
                neighbours: List[Cell] = list(filter(lambda c: not c.collapsed, self.getNeighbours(cell.row, cell.col)))
                if len(neighbours) == 0:
                    continue

                for neighbour_cell in neighbours:
                    delta_row = neighbour_cell.row - cell.row
                    delta_col = neighbour_cell.col - cell.col
                    if delta_row != 0:
                        direction = f"{'pos' if delta_row > 0 else 'neg'}-y"
                    else:
                        direction = f"{'pos' if delta_col > 0 else 'neg'}-x"
                    edge_label = cell.getEdge(direction)
                    neighbour_cell.reduce(edge_label[::-1], self.reverse_direction(direction))
                    # [::-1] reverses the string this is required for asymmetrical labels
                    if neighbour_cell.entropy == 1:  # Tile has only one tile available
                        neighbour_cell.collapse()
                    elif neighbour_cell.entropy == 0 and not neighbour_cell.collapsed:  # Tile has no options
                        invalidState = True
            idx += 1

        return invalidState

    def stateComplete(self) -> bool:
        complete = True
        idx = 0
        while idx < len(self.board) and complete:
            if not self.board[idx].collapsed:
                complete = False
            idx += 1
        print(complete, self.board)
        return complete

    def stateInvalid(self) -> bool:
        invalid = False
        idx = 0
        while idx < len(self.board) and not invalid:
            if self.board[idx].entropy == 0 and not self.board[idx].collapsed:
                invalid = True

            idx += 1

        return invalid
