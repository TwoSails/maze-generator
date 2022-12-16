"""
File: MazeGenerator.py
Created: 22/11/22
"""
from mazeGenerator.controllers.board import Board
from mazeGenerator.models import Tile
from mazeGenerator.config import Config
from mazeGenerator.response import Response, Ok, Err
from mazeGenerator.response import TileSetDoesNotExist, InvalidState

from typing import List
import json
import os


class App:
    def __init__(self):
        self.board = Board()
        self.config = Config()
        self.tileSet: List[Tile] = []

    def loadTileSet(self, tileSet, transform: bool = True) -> Response:
        """
        Loads all tiles into the algorithm
        :param tileSet: Name of the tile set
        :param transform: Automatically apply the transformations to all tiles
        :return: Success
        """
        if tileSet not in os.listdir(self.config.get("dataPath")):
            return Err(TileSetDoesNotExist)

        with open(f"{self.config.get('dataPath')}{tileSet}/tiles.json") as tileSetConfigFile:
            tileSetConfig = json.load(tileSetConfigFile)

        for tile in tileSetConfig["tiles"]:
            if not tile["active"]:
                continue
            self.tileSet.append(Tile())
            res = self.tileSet[-1].setTileSet(tileSet)
            if not res.success:
                return res

            res = self.tileSet[-1].setName(tile["name"])
            if not res.success:
                return res

            res = self.tileSet[-1].loadImage()
            if not res.success:
                return res

        if transform:
            self.transformTileSet()

        return Ok()

    def transformTileSet(self):
        """
        Applies transformations to the tiles loaded
        :return:
        """
        expansion = []
        for tile in self.tileSet:
            tile.applyTransformations()
            expansion.extend(tile.expand())
        self.tileSet.extend(expansion)

    def setupBoard(self, height, width, seed=0):
        """
        Configures the dimensions to create the board and adds the tile set to the algorithm
        :param height:
        :param width:
        :param seed:
        :return:
        """
        if len(self.tileSet) == 0:
            return Err(TileSetDoesNotExist)
        self.board.setHeight(height)
        self.board.setWidth(width)
        self.board.tileSet = self.tileSet
        self.board.setSeed(seed)
        self.board.generateBoard()

    def run(self) -> Response:
        """
        Performs collapse
        :return: Cell Board | InvalidState
        """
        self.board.performCollapse()
        if self.board.collapsed:
            return Ok(self.board.board)

        return Err(InvalidState if self.board.stateInvalid() else None, data=self.board.board)
