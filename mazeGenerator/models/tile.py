"""
File: tile.py
Date Created: 31/10/22
Description: This is the Tile class which handles the single tile with composition of edges and transformations
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
        """
        Fixes config path
        :return:
        """
        dataPath = self.__config.get("dataPath")
        if dataPath[-1] != "/":
            dataPath = f"{dataPath}/"

        return dataPath

    def setName(self, name: str) -> Response:
        """
        Setter method which validates the tile being loading exists
        :param name: Tile name
        :return: Response
        """
        if self.__tileSetName == "":
            return Err(TileNameNotSet)
        if name not in os.listdir(self.makeFilePath()):
            return Err(TileDoesNotExist)
        self.__name = name
        return Ok(name)

    def getName(self) -> str:
        """
        Getter method for tile name
        :return: tile name
        """
        return self.__name

    def setTileSet(self, name: str) -> Response:
        """
        Setter method for tile set name with validation
        :param name:
        :return:
        """
        if name not in os.listdir(self.__config.get("dataPath")):
            return Err(TileSetDoesNotExist)
        self.__tileSetName = name
        return Ok(name)

    def getTileSet(self) -> str:
        return self.__tileSetName

    def setResolution(self, res: int) -> Response:
        """
        Setter method with validation for inputted resolution
        :param res: Pixel resolution of tile
        :return:
        """
        if isinstance(res, str):
            try:
                res = int(res)
            except ValueError:
                return Err(InvalidResolution)

        res = abs(res)
        if res <= 0:
            return Err(InvalidResolution)

        self.__resolution = res
        return Ok(self.__resolution)

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

    def getEdge(self, direction: str):
        pass

    def applyTransformations(self):
        pass
