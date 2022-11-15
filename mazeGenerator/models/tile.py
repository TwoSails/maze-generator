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
from mazeGenerator.data import Rotation, Axis
from mazeGenerator.response.response import Ok, Err, Response
from mazeGenerator.response.exceptions import InvalidResolution, TileNameNotSet, TileDoesNotExist, \
        TileSetDoesNotExist, InvalidEdgeLabel, TileNotLoaded


class Tile:
    def __init__(self) -> None:
        self.__config: Config = Config()
        self.__transformations: List[Rotation | Axis] = []  # List of available transformations
        self.__edges: List[Edge] = []
        self.__image = None
        self.__filePath: str = self.__setBasePath()
        self.__tileSetName: str = ""
        self.__name: str = ""
        self.__resolution: int = 3  # Label resolution of edge labels

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

    def getEdge(self, direction: str) -> Response:
        edges = ["pos-x", "pos-y", "neg-x", "neg-y"]
        if direction.lower() not in edges:
            return Err(InvalidEdgeLabel)

        pass

    def applyTransformations(self):
        if len(self.__edges) == 0:
            return Err(TileNotLoaded)

        transform = Transformation(self.__edges[0])
        for transformation in self.__transformations:
            if isinstance(transformation, Rotation):
                self.__edges.append(transform.rotate(transformation))
            elif isinstance(transformation, Axis):
                self.__edges.append(transform.reflect(transformation))

        return Ok(self.__edges)
