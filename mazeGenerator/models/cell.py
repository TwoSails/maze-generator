"""
File: cell.py
Date Created: 19/11/22
"""
from mazeGenerator.models import Tile, Transformation
from mazeGenerator.response import Response, Ok, Err, InvalidState
from typing import List
from random import choice


class Cell:
    def __init__(self, tileSet: List[Tile], row: int = -1, col: int = -1):
        self.collapsed: bool = False
        self.__entropy: int = int(1e9)
        self.availableTiles: List[Tile] = tileSet
        self.__transformation: Transformation | None = None
        self.tile: Tile | None = None
        self.row: int = row
        self.col: int = col

    def __repr__(self):
        return f"Cell<{self.collapsed=}, {self.entropy=}, {self.tile=}, {self.transformation=} {self.row}-{self.col}>"

    @property
    def transformation(self):
        if self.tile is None:
            return None
        return self.tile.getTransformation()

    @property
    def entropy(self) -> int:
        self.__entropy = len(self.availableTiles)
        return self.__entropy

    @entropy.setter
    def entropy(self, i: int):
        self.__entropy = i

    def getTile(self) -> Tile:
        return self.tile

    def getEdge(self, direction: str) -> str:
        if self.tile is None:
            return ""

        edge = self.tile.getEdge(direction, self.transformation)
        if edge.success:
            return edge.data

        return ""

    def collapse(self) -> Response:
        if len(self.availableTiles) == 0:
            return Err(InvalidState)

        self.tile = choice(self.availableTiles)
        self.collapsed = True
        self.availableTiles = [self.tile]  # This overwrites the calculation for entropy so sets cell entropy to 1

        return Ok(self.tile)

    def reduce(self, edge_label, direction):
        self.availableTiles = list(filter(lambda tile: tile.getEdge(direction).data == edge_label, self.availableTiles))
