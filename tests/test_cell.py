import unittest

from mazeGenerator.models import Cell, Tile
from mazeGenerator import App


class TestCell(unittest.TestCase):
    def test_load_Cell(self):
        """
        1 - Tests that the Cell is loaded with collapsed as default
        """
        app = App()
        app.loadTileSet("default")
        cell: Cell = Cell(app.tileSet)
        self.assertFalse(cell.collapsed)

    def test_calculate_entropy(self):
        """
        2 - Test that the cell returns the correct entropy
        """
        app = App()
        app.loadTileSet("default")
        cell: Cell = Cell(app.tileSet)
        self.assertEqual(len(app.tileSet), cell.entropy)

    def test_calculate_empty_entropy(self):
        """
        3 - Test that cell returns 0 entropy
        """
        cell: Cell = Cell([])
        self.assertEqual(cell.entropy, 0)

    def test_get_not_collapsed_tile(self):
        """
        4 - Null tile due to not collapsed
        """
        app = App()
        app.loadTileSet("default")
        cell: Cell = Cell(app.tileSet)
        self.assertTrue(cell.getTile() is None)

    def test_get_collapsed_tile(self):
        """
        5 - Get tile when collapsed
        """
        app = App()
        app.loadTileSet("default")
        cell: Cell = Cell(app.tileSet)
        cell.collapse()
        self.assertTrue(cell.getTile() is not None)

    def test_get_not_collapsed_edge(self):
        """
        6 - Get edge when not collapsed
        """
        app = App()
        app.loadTileSet("default")
        cell: Cell = Cell(app.tileSet)
        self.assertTrue(cell.getEdge("pos-x") == "")

    def test_get_collapsed_edge(self):
        """
        7 - Get edge when collapsed
        """
        app = App()
        app.loadTileSet("default")
        cell: Cell = Cell(app.tileSet)
        cell.collapse()
        self.assertTrue(cell.getEdge("pos-x") != "")

    def test_collapse_empty_cell(self):
        """
        8 - Collapse empty tile
        """
        cell: Cell = Cell([])
        cell.collapse()
        self.assertTrue(cell.entropy == 0)

    def test_collapse_single_cell(self):
        """
        9 - Collapse single tile
        """
        cell: Cell = Cell([Tile()])
        cell.collapse()
        self.assertTrue(cell.entropy == 1)

    def test_collapse_multi_cell(self):
        """
        10 - Collapse multi tile
        """
        app = App()
        app.loadTileSet("default")
        cell: Cell = Cell(app.tileSet)
        cell.collapse()
        self.assertTrue(cell.entropy == 1)

    def test_reduce_edge_label(self):
        """
        11 - Reduce with blank edge label
        """
        app = App()
        app.loadTileSet("default")
        cell: Cell = Cell(app.tileSet)
        cell.reduce("000", "pos-x")
        self.assertLess(cell.entropy, len(app.tileSet))
