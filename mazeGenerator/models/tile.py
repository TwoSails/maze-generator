"""
File: tile.py
Date Created: 31/10/22
Description: This file will contain the tile class
"""
# Python Modules
import os
from typing import List

# External Modules

# Local Modules
from mazeGenerator.config import Config
from mazeGenerator.models.edge import Edge
from mazeGenerator.models.transformations import Transformation
from mazeGenerator.response.response import Ok, Err, Response
from mazeGenerator.response.exceptions import InvalidResolution, TileNameNotSet, TileDoesNotExist, TileSetDoesNotExist


class Tile:
    def __init__(self) -> None:
        self.__config: Config = Config()
        self.__transformations: List[Transformation] = []
        self.__edges: List[Edge] = []
        self.__image = None
        self.__filePath: str = self.__setBasePath()
        self.__tileSetName: str = ""
        self.__name: str = ""
        self.__resolution: int = 3

    def __setBasePath(self) -> str:
        dataPath = self.__config.dataPath
        if dataPath[-1] != "/":
            dataPath = f"{dataPath}/"

        return dataPath

    def setName(self, name: str) -> Response:
        if self.__tileSetName == "":
            return Err(TileNameNotSet)
        if name not in os.listdir(self.makeFilePath()):
            return Err(TileDoesNotExist)
        self.__name = name
        return Ok(name)

    def getName(self) -> str:
        return self.__name

    def setTileSet(self, name: str):
        if name not in os.listdir(self.__config.dataPath):
            return Err(TileSetDoesNotExist)
        self.__tileSetName = name
        return Ok(name)

    def getTileSet(self) -> str:
        return self.__tileSetName

    def setResolution(self, res: int):
        if isinstance(res, str):
            try:
                res = int(res)
            except ValueError:
                return Err(InvalidResolution)

        res = abs(res)
        if res <= 0:
            return Err(InvalidResolution)

        self.__resolution = res
        return self.__resolution

    def getResolution(self) -> int:
        return self.__resolution

    def makeFilePath(self, name: str = "", tileSet: str = "") -> str:
        if tileSet == "":
            tileSet = self.__tileSetName
        if name == "":
            name = self.__name
        return f"{self.__filePath}{tileSet}{f'/{name}' if name != '' else ''}"

    def loadImage(self):
        pass

    def getEdge(self, dir: str):
        pass

    def applyTransformations(self):
        pass

