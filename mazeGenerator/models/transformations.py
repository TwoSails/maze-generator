"""
File: transformations.py
Date Created: 10/11/22
Description: Contains the transformations class which holds data and methods on how to transform an edge
"""
# Python Modules
from typing import List
# Local Imports
from mazeGenerator.data import Rotation, Axis
from mazeGenerator.models import Edge


class Transformation:
    def __init__(self, edge: Edge):
        self.__edge = edge  # Base edge labels for transformations to be applied to

    def rotate(self, angle: Rotation):
        """
        Method which rotates the edge labels of the edge attribute
        :param angle: Transformation angle
        :return: Transformed edge labels
        """
        edge = Edge()
        match angle:
            case Rotation.one:  # Rotate 90 degrees clockwise
                edge.xAxis = self.__edge.yAxis
                edge.yAxis = list(reversed(self.__edge.xAxis))

            case Rotation.two:  # Rotate 180 degrees clockwise
                edge.xAxis = list(reversed(self.__edge.xAxis))
                edge.yAxis = list(reversed(self.__edge.yAxis))

            case Rotation.three:  # Rotate 270 degrees clockwise
                edge.xAxis = list(reversed(self.__edge.yAxis))
                edge.yAxis = self.__edge.xAxis

            case _:
                pass

        edge.transformation = angle

        return edge

    def reflect(self, axis: Axis) -> Edge:
        """
        Method which reflects the edge labels along an axis
        :param axis: transformation axis
        :return: Edge
        """
        edge = Edge()
        match axis:
            case Axis.X:
                edge.xAxis = [pos[::-1] for pos in self.__edge.xAxis]
                edge.yAxis = [pos[::-1] for pos in reversed(self.__edge.yAxis)]

            case Axis.Y:
                edge.xAxis = [pos[::-1] for pos in reversed(self.__edge.xAxis)]
                edge.yAxis = [pos[::-1] for pos in self.__edge.yAxis]

        edge.transformation = axis

        return edge

    def transform(self) -> List[Edge]:
        """
        Method which applies all transformations on an edge object
        :return: List of edge objects with transformations applied
        """
        transformations = []
        for angle in [Rotation.one, Rotation.two, Rotation.three]:
            transformations.append(self.rotate(angle))

        for axis in [Axis.X, Axis.Y]:
            transformations.append(self.reflect(axis))

        return transformations
