"""
File: MazeGenerator.py
Created: 22/11/22
"""
from mazeGenerator.controllers.board import Board
from mazeGenerator.models import Tile
from mazeGenerator.config import Config
from mazeGenerator.response import Response, Ok, Err
from mazeGenerator.response import TileSetDoesNotExist

from typing import List
import json
import os


class App:
    def __init__(self):
        self.board = Board()
        self.config = Config()
        self.tileSet: List[Tile] = []

    def loadTileSet(self, tileSet) -> Response:
        if tileSet not in os.listdir(self.config.get("dataPath")):
            return Err(TileSetDoesNotExist)

        with open(f"{self.config.get('dataPath')}{tileSet}/tiles.json") as tileSetConfigFile:
            tileSetConfig = json.load(tileSetConfigFile)

        for tile in tileSetConfig["tiles"]:
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

        return Ok()

    def transformTileSet(self):
        expansion = []
        for tile in self.tileSet:
            tile.applyTransformations()
            expansion.extend(tile.expand())
        self.tileSet.extend(expansion)

    def setupBoard(self, height, width):
        if len(self.tileSet) == 0:
            return Err(TileSetDoesNotExist)
        self.board.setHeight(height)
        self.board.setWidth(width)
        self.board.tileSet = self.tileSet
        self.board.generateBoard()

    def run(self):
        self.board.performCollapse()
        print("eh")
