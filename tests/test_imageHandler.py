import unittest

from mazeGenerator import App
from mazeGenerator.controllers import ImageHandler
from mazeGenerator.data import Rotation


class TestImageHandler(unittest.TestCase):
    def test_set_valid_tiles(self):
        """
        1 - Set valid tiles
        """
        app = App()
        img = ImageHandler()
        app.loadTileSet("default", False)
        res = img.SetTiles(app.tileSet)
        self.assertTrue(res.success)

    def test_set_invalid_tiles(self):
        """
        2 - Set invalid tiles
        """
        img = ImageHandler()
        res = img.SetTiles(["01"])
        self.assertFalse(res.success)

    def test_set_valid_width(self):
        """
        3 - Set Valid Width
        """
        img = ImageHandler()
        res = img.SetWidth(50)
        self.assertTrue(res.success)

    def test_set_str_width(self):
        """
        4 - Set valid string width
        """
        img = ImageHandler()
        res = img.SetWidth("50")
        self.assertTrue(res.success)

    def test_set_invalid_width(self):
        """
        5 - Set invalid width
        """
        img = ImageHandler()
        res = img.SetWidth("a")
        self.assertFalse(res.success)

    def test_set_valid_height(self):
        """
        6 - Set valid height
        """
        img = ImageHandler()
        res = img.SetHeight(50)
        self.assertTrue(res.success)

    def test_set_str_height(self):
        """
        7 - Set valid string height
        """
        img = ImageHandler()
        res = img.SetHeight("50")
        self.assertTrue(res.success)

    def test_set_invalid_height(self):
        """
        8 - Set invalid height
        """
        img = ImageHandler()
        res = img.SetHeight('a')
        self.assertFalse(res.success)

    def test_set_valid_tile_image_resolution(self):
        """
        9 - Set valid tile image resolution
        """
        img = ImageHandler()
        res = img.SetTileImageResolution(3)
        self.assertTrue(res.success)

    def test_set_invalid_tile_image_resolution(self):
        """
        10 - Set invalid tile image resolution
        """
        img = ImageHandler()
        res = img.SetTileImageResolution("a")
        self.assertFalse(res.success)

    def test_get_valid_index(self):
        """
        11 - Get valid index
        """
        img = ImageHandler(height=50, width=50)
        res = img.GetIdx(row=0, col=1)
        self.assertTrue(res.success and res.data == 1)

    def test_get_invalid_index(self):
        """
        12 - Get invalid index
        """
        img = ImageHandler(height=50, width=50)
        res = img.GetIdx(row=-1, col=-1)
        self.assertFalse(res.success)

    def test_generate_undefined_blank_image(self):
        """
        13 - Generate blank image prior setting dimensions
        """
        img = ImageHandler()
        before = img.maze
        res = img.GenerateBlankImage()
        self.assertFalse(res.success and before == img.maze)

    def test_generate_defined_blank_image(self):
        """
        14 - Generate blank image after setting dimensions
        """
        img = ImageHandler(height=50, width=50, tileImageResolution=3)
        before = img.maze
        res = img.GenerateBlankImage()
        self.assertTrue(res.success and before != img.maze)

    def test_place_valid_cell(self):
        """
        15 - Place valid cell
        """
        app = App()
        app.loadTileSet("default")
        app.setupBoard(50, 50)
        img = ImageHandler(height=50, width=50, tileImageResolution=3)
        img.GenerateBlankImage()
        img.board = app.board.board
        res = img.PlaceCell(1, 1)
        self.assertTrue(res.success)

    def test_place_invalid_cell(self):
        """
        16 - Place invalid cell
        """
        app = App()
        app.setupBoard(50, 50)
        img = ImageHandler(height=50, width=50, tileImageResolution=3)
        img.GenerateBlankImage()
        img.board = app.board.board
        res = img.PlaceCell(-1, -1)
        self.assertFalse(res.success)

    def test_transform_valid(self):
        """
        17 - Transform valid transformation
        """
        app = App()
        app.loadTileSet("default")
        img = ImageHandler()
        transform = img.TransformTileImage(Rotation.two, app.tileSet[0])
        self.assertNotEqual(transform, None)

    def test_transform_invalid(self):
        """
        18 - Transform invalid transformation
        """
        app = App()
        app.loadTileSet("default")
        img = ImageHandler()
        transform = img.TransformTileImage("Rotation.two", app.tileSet[0])
        self.assertEqual(transform, None)

    def test_save_image(self):
        """
        19 - Save image
        """
        img = ImageHandler(width=50, height=50, tileImageResolution=3, tileSetName="default")
        app = App()
        app.loadTileSet("default")
        img.SetTiles(app.tileSet)
        img.GenerateBlankImage()
        res = img.SaveImage()
        self.assertTrue(res.success)

    def test_generate_image_defined(self):
        """
        20 - Generate Image with configured settings
        """
        img = ImageHandler(width=50, height=50, tileImageResolution=3, tileSetName="default")
        app = App()
        app.loadTileSet("default")
        img.SetTiles(app.tileSet)
        img.GenerateImage()
        self.assertTrue(True)

    def test_generate_image_undefined(self):
        """
        21 - Generate Image without Configured settings
        """
        img = ImageHandler()
        with self.assertRaises(AttributeError):
            img.GenerateImage()


if __name__ == '__main__':
    unittest.main()
