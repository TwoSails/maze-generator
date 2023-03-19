"""
File: rotation.py
Date Created: 12/11/22
Description: Contains the Rotation object listing possible rotation transformations
"""
from enum import Enum


class Rotation(Enum):
    """
    Represents the angle of rotation being applied in 90 degrees
    """
    zero = 0
    one = 1
    two = 2
    three = 3
