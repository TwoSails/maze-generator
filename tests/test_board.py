import unittest

from mazeGenerator.controllers import Board
from mazeGenerator.models import Tile


class TestBoard(unittest.TestCase):
    def test_valid_width(self):
        """
        1 - Set correct width
        """
        board = Board()
        res = board.setWidth(50)
        self.assertTrue(res.success)

    def test_out_of_bounds_width(self):
        """
        2 - Set out of range width
        """
        board = Board()
        res = board.setWidth(101)
        self.assertFalse(res.success)

    def test_invalid_data_type_width(self):
        """
        3 - Set invalid data type width
        """
        board = Board()
        res = board.setWidth("50")
        self.assertFalse(res.success)

    def test_valid_height(self):
        """
        4 - Set correct height
        """
        board = Board()
        res = board.setHeight(50)
        self.assertTrue(res.success)

    def test_out_of_bounds_height(self):
        """
        5 - Set out of range height
        """
        board = Board()
        res = board.setHeight(101)
        self.assertFalse(res.success)

    def test_invalid_data_type_height(self):
        """
        6 - Set invalid data type height
        """
        board = Board()
        res = board.setHeight("50")
        self.assertFalse(res.success)

    def test_get_valid_idx(self):
        """
        7 - Get board index
        """
        board = Board()
        board.setHeight(50)
        board.setWidth(50)
        board.generateBoard()
        res = board.getIdx(0, 1)
        self.assertTrue(res.data == 1 and res.success)

    def test_get_out_of_bounds_idx(self):
        """
        8 - Get out of range index
        """
        board = Board()
        board.setHeight(50)
        board.setWidth(50)
        board.generateBoard()
        res = board.getIdx(51, 1)
        self.assertFalse(res.success)

    def test_get_valid_neighbours(self):
        """
        9 - Get neighbours of corner
        """
        board = Board()
        board.setHeight(50)
        board.setWidth(50)
        board.generateBoard()
        neighbours = board.getNeighbours(0, 0)
        self.assertTrue(len(neighbours) == 4, msg=f"{neighbours}")

    def test_get_invalid_neighbours(self):
        """
        10 - Get neighbours of invalid
        """
        board = Board()
        board.setHeight(50)
        board.setWidth(50)
        board.generateBoard()
        neighbours = board.getNeighbours(100, 100)
        self.assertTrue(len(neighbours) == 4, msg=f"{neighbours}")

    def test_find_default_lowest_entropy(self):
        """
        11 - Find lowest entropy
        """
        board = Board()
        board.setHeight(50)
        board.setWidth(50)
        board.generateBoard()
        res = board.findLowestEntropy()
        self.assertTrue(res.success and res.data.row == 0 and res.data.col == 0)

    def test_state_complete(self):
        """
        12 - State Complete
        """
        board = Board()
        board.setHeight(50)
        board.setWidth(50)
        board.generateBoard()
        complete = board.stateComplete()
        self.assertFalse(complete)

    def test_state_invalid(self):
        """
        13 - State Invalid
        """
        board = Board()
        board.tileSet = [Tile()]
        board.setHeight(50)
        board.setWidth(50)
        board.generateBoard()
        invalid = board.stateInvalid()
        self.assertFalse(invalid)
