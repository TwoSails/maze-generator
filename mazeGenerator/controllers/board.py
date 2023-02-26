"""
File: board.py
Date Created: 19/11/22
"""
import random
import pickle

from mazeGenerator.config import Config
from mazeGenerator.models import Tile, Cell
from mazeGenerator.response import Response, Ok, Err
from mazeGenerator.response import ExceedsBounds, EmptyBoard
from mazeGenerator.response.pool import OkResponse

from mazeGenerator.controllers.boardHelper import getNeighbourIndexes

from typing import List


class Board:
    def __init__(self):
        self.__config: Config = Config()
        self.height: int = 0  # Width
        self.width: int = 0
        self.tileSet: List[Tile] = []
        self.board: List[Cell] = []
        self.idxCache = {}
        self.neighbourCache = {}
        self.collapsed = False
        self.seed = 0
        self.logging = False
        self.log = []

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

    def setSeed(self, seed: str | int):
        self.seed = seed

    def getIdx(self, row: int, col: int) -> Response:
        if row > self.height or col > self.width or row < 0 or col < 0:
            return Err(ExceedsBounds)

        if f"{row}-{col}" in self.idxCache.keys():
            return OkResponse(self.idxCache[f"{row}-{col}"])

        idx = (row * self.width + col)
        self.idxCache[f"{row}-{col}"] = idx
        return OkResponse(idx)

    def getNeighbours(self, row: int, col: int) -> List[Cell]:
        if f"{row}-{col}" in self.neighbourCache.keys():
            return self.neighbourCache[f"{row}-{col}"]
        neighboursIdx = getNeighbourIndexes(row, col, self.width, self.height)

        neighbours_new = [self.board[idx] for idx in neighboursIdx if idx != -1]
        self.neighbourCache[f"{row}-{col}"] = neighbours_new
        return neighbours_new

    def generateBoard(self):
        if self.seed == 0 or self.seed == "":
            self.seed = "".join([str(random.randint(0, 10)) for _ in range(10)])
        for row in range(self.height):
            for col in range(self.width):
                self.board.append(Cell(self.tileSet, row=row, col=col, seed=self.seed))
                self.board[-1].setSeed()

    def findLowestEntropy(self) -> Response:
        if len(self.board) == 0:
            return Err(EmptyBoard)
        lowestEntropy = self.board[0]
        for cell in list(filter(lambda c: not c.collapsed, self.board)):
            if ((cell.entropy < lowestEntropy.entropy and not cell.collapsed)
                    or (not cell.collapsed and lowestEntropy.collapsed)):
                # This was the line of code which posed the most issues due to it overwriting lowest cell with collapsed
                # cells and hence creating an infinite loop
                # defining condition being "and not cell.collapsed"
                lowestEntropy = cell

        return Ok(lowestEntropy)

    def performCollapse(self):
        invalid = False
        while not invalid and not self.collapsed:
            invalid = self.calculateEntropy()
            if self.stateComplete():
                self.collapsed = True

            lowestCell = self.findLowestEntropy()
            if lowestCell.success:
                lowestCell.data.collapse()

            if self.logging:
                # That's one way to make it thread safe i guess...
                # Issue was caused by deepcopy due to lack of thread safety in method
                # Deepcopy therefore caused the program to become unresponsive
                self.log = self.log[:] + [pickle.loads(pickle.dumps(self.board))]
                # self.log.append(pickle.loads(pickle.dumps(self.board)))

        self.board[0].getEdge("pos-x")

    @staticmethod
    def reverse_direction(direction):
        flip = {"pos": "neg", "neg": "pos"}
        direction = direction.split("-")
        direction[0] = flip[direction[0]]
        return "-".join(direction)

    def calculateEntropy(self):
        invalidState = False
        idx = 0
        # for cell in filter(lambda c: c.collapsed, self.board):
        #     pass
        while not invalidState and idx < len(self.board):
            cell = self.board[idx]
            if cell.collapsed:
                neighbours: List[Cell] = list(filter(lambda c: not c.collapsed, self.getNeighbours(cell.row, cell.col)))
                if len(neighbours) == 0:
                    idx += 1
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

        return complete

    def stateInvalid(self) -> bool:
        invalid = False
        idx = 0
        while idx < len(self.board) and not invalid:
            if self.board[idx].entropy == 0 and not self.board[idx].collapsed:
                invalid = True

            idx += 1

        return invalid
