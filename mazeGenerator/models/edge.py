"""
File: edge.py
Date Created: 31/10/22
Description: Contains the Edge class which holds the labels to annotate the edges of a tile
"""
from mazeGenerator.data import Rotation, Axis


class Edge:
    def __init__(self,
                 *args,
                 x: list[str] | None = None,
                 y: list[str] | None = None,
                 pX="", pY="", nX="", nY="",
                 transformation: Rotation | Axis = None):
        """
        Constructor method with options on how to load the data
        :param x: List of x-axis edge labels
        :param y: List of y-axis edge labels
        :param pX:
        :param pY:
        :param nX:
        :param nY:
        :param transformation: the transformation applied to the edge
        """
        self.xAxis = [""] * 2
        self.yAxis = [""] * 2

        # This is important to understand how the tile got here
        self.transformation = transformation

        if pX != self.xAxis[1]:
            self.xAxis[1] = pX
        if pY != self.yAxis[1]:
            self.yAxis[1] = pY
        if nX != self.yAxis[0]:
            self.xAxis[0] = nX
        if nY != self.yAxis[0]:
            self.yAxis[0] = nY

        if x is not None:
            self.xAxis = x
        if y is not None:
            self.yAxis = y
        if len(args) == 4:
            self.yAxis = [args[3], args[1]]
            self.xAxis = [args[2], args[0]]

        for i, x in enumerate(self.xAxis):
            if not isinstance(x, str):
                self.xAxis[i] = ""

        for i, y in enumerate(self.yAxis):
            if not isinstance(y, str):
                self.yAxis[i] = ""

    def positiveX(self):
        """
        Getter Method
        :return: Positive X Axis edge label
        """
        return self.xAxis[1]

    def negativeX(self):
        """
        Getter Method
        :return: Negative X Axis edge label
        """
        return self.xAxis[0]

    def positiveY(self):
        """
        Getter Method
        :return: Positive Y Axis edge label
        """
        return self.yAxis[1]

    def negativeY(self):
        """
        Getter Method
        :return: Negative Y Axis edge label
        """
        return self.yAxis[0]
