import unittest

from mazeGenerator.models import Tile


class TestTile(unittest.TestCase):
    def test_set_valid_tile_set(self):
        """
        1 - Tests tile set name is accepted
        """
        tile = Tile()
        res = tile.setTileSet("default")

        self.assertTrue(res.success)

    def test_set_empty_tile_set(self):
        """
        2 - Tests setting tile set with empty argument
        """
        tile = Tile()
        res = tile.setName("")
        self.assertFalse(res.success)

    def test_set_invalid_tile_set(self):
        """
        3 - Tests tile set name is rejected
        """
        tile = Tile()
        res = tile.setTileSet("wave")

        self.assertFalse(res.success)

    def test_set_valid_name(self):
        """
        4 - Tests name is set if valid
        """
        tile = Tile()
        tile.setTileSet("default")
        res = tile.setName("01")

        self.assertTrue(res.success)

    def test_set_empty_name(self):
        """
        5 - Tests setting name when argument is empty
        """
        tile = Tile()
        tile.setTileSet("default")
        res = tile.setName("")

        self.assertFalse(res.success)

    def test_set_format_name(self):
        """
        6 - Short string inputted to set name
        """
        tile = Tile()
        tile.setTileSet("default")
        res = tile.setName("1")

        self.assertTrue(res.success)

    def test_set_invalid_name(self):
        """
        7 - Tests name is set if invalid
        """
        tile = Tile()
        tile.setTileSet("default")
        res = tile.setName("23")

        self.assertFalse(res.success)

    def test_get_valid_name(self):
        """
        8 - Tests fetching of valid tile set name
        """
        tile = Tile()
        name = "01"
        tile.setTileSet("default")
        tile.setName(name)
        self.assertEqual(tile.getName(), name)

    def test_get_invalid_name(self):
        """
        9 - Tests fetching of unset tile name
        """
        tile = Tile()
        tile.setTileSet("default")
        self.assertEqual(tile.getName(), "")

    def test_get_valid_tile_set(self):
        """
        10 - Tests fetching of valid tile set name
        """
        tile = Tile()
        name = "default"
        tile.setTileSet(name)
        self.assertEqual(tile.getTileSet(), name)

    def test_get_invalid_tile_set(self):
        """
        11 - Tests fetching of unset tile set name
        """
        tile = Tile()
        self.assertEqual(tile.getTileSet(), "")

    def test_set_valid_int_resolution(self):
        """
        12 - Tests setting resolution with valid integer
        :return:
        """
        tile = Tile()
        res = tile.setResolution(3)
        self.assertTrue(res.success)

    def test_set_invalid_small_int_resolution(self):
        """
        13 - Tests setting resolution with valid integer
        :return:
        """
        tile = Tile()
        res = tile.setResolution(0)
        self.assertFalse(res.success)

    def test_set_valid_string_resolution(self):
        """
        14 - Tests setting resolution with valid string
        :return:
        """
        tile = Tile()
        res = tile.setResolution("3")
        self.assertTrue(res.success)

    def test_set_invalid_string_resolution(self):
        """
        15 - Tests setting resolution with invalid string
        :return:
        """
        tile = Tile()
        res = tile.setResolution("a")
        self.assertFalse(res.success)

    def test_get_valid_resolution(self):
        """
        16 - Get Resolution after set resolution
        :return:
        """
        tile = Tile()
        tile.setResolution(3)
        res = tile.getResolution()
        self.assertEqual(res, 3)

    def test_get_invalid_resolution(self):
        """
        17 - Get Resolution before set resolution
        :return:
        """
        tile = Tile()
        res = tile.getResolution()
        self.assertEqual(res, 3)

    def test_invalid_make_path(self):
        """
        18 - makeFilePath before tileSet or name
        :return:
        """
        tile = Tile()
        res = tile.makeFilePath()
        self.assertEqual(res, "")

    def test_valid_make_path(self):
        """
        19 - makeFilePath after tileSet and name
        :return:
        """
        tile = Tile()
        res = tile.makeFilePath("01", "default")
        self.assertNotEqual(res, "")

    def test_get_edge(self):
        """
        20 - get valid edge
        :return:
        """
        tile = Tile()
        tile.setTileSet("default")
        tile.setName("01")
        imgRes = tile.loadImage()
        res = tile.getEdge("pos-x", None)
        self.assertTrue(res.success)

    def test_get_invalid_edge(self):
        """
        21 - get invalid edge
        """
        tile = Tile()
        res = tile.getEdge("pos-z", None)
        self.assertFalse(res.success)

    def test_load_invalid_image(self):
        """
        22 - Call LoadImage without set name
        """
        tile = Tile()
        res = tile.loadImage()
        self.assertFalse(res.success)

    def test_load_valid_image(self):
        """
        23 - Call LoadImage with set name
        """
        tile = Tile()
        tile.setTileSet("default")
        tile.setName("01")
        res = tile.loadImage()
        self.assertTrue(res.success)


if __name__ == '__main__':
    unittest.main()
