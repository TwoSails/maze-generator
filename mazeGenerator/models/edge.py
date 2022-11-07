"""
File: edge.py
Date Created: 31/10/22
Description: Contains the Edge class which holds the labels to annotate the edges of a tile
"""


class Edge:
    def __init__(self,
                 *args,
                 x: list[str] | None = None,
                 y: list[str] | None = None,
                 pX="", pY="", nX="", nY=""):
        """
        Constructor method with options on how to load the data
        :param x: List of x-axis edge labels
        :param y: List of y-axis edge labels
        :param pX:
        :param pY:
        :param nX:
        :param nY:
        """
        self.__xAxis = [""] * 2
        self.__yAxis = [""] * 2

        if pX != self.__xAxis[1]:
            self.__xAxis[1] = pX
        if pY != self.__yAxis[1]:
            self.__yAxis[1] = pY
        if nX != self.__yAxis[0]:
            self.__xAxis[0] = nX
        if nY != self.__yAxis[0]:
            self.__yAxis[0] = nY

        if x is not None:
            self.__xAxis = x
        if y is not None:
            self.__yAxis = y
        if len(args) == 4:
            self.__yAxis = [args[3], args[1]]
            self.__xAxis = [args[2], args[0]]

        print(self.__yAxis, self.__xAxis)

    def positiveX(self):
        """
        :return: Positive X Axis edge label
        """
        return self.__xAxis[1]

    def negativeX(self):
        """
        :return: Negative X Axis edge label
        """
        return self.__xAxis[0]

    def positiveY(self):
        """
        :return: Positive Y Axis edge label
        """
        return self.__yAxis[1]

    def negativeY(self):
        """
        :return: Negative Y Axis edge label
        """
        return self.__yAxis[0]
