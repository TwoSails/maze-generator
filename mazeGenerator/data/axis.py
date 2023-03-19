"""
File: axis.py
Date Created: 12/11/22
Description: Contains the Axis object listing possible reflection transformations
"""
from enum import Enum


class Axis(Enum):
    """
    Represents the transformation axis for reflection
    """
    X = 100
    Y = 101
