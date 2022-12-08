import unittest

from mazeGenerator import App


class TestMazeGenerator(unittest.TestCase):
    def test_set_correct_tile_set(self):
        """
        1 - Set correct tile set
        """
        app = App()
        res = app.loadTileSet("default")
        self.assertTrue(res.success)

    def test_set_invalid_tile_set(self):
        """
        2 - Set invalid tile set
        """
        app = App()
        res = app.loadTileSet("WFC")
        self.assertFalse(res.success)

    def test_transform_tile_set(self):
        """
        3 - Transform tile set
        """
        app = App()
        app.loadTileSet("default", False)
        before = len(app.tileSet)
        app.transformTileSet()
        after = len(app.tileSet)
        self.assertTrue(after > before)
        

if __name__ == '__main__':
    unittest.main()
