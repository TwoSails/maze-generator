import unittest

from mazeGenerator.models import Transformation, Tile
from mazeGenerator.data import Rotation, Axis


class TestTransformation(unittest.TestCase):
    @staticmethod
    def setup_tile():
        tile = Tile()
        tile.setTileSet("default")
        tile.setName("06")
        tile.loadImage()
        return tile, {"a": tile.getEdge("pos-y", None).data,
                      "b": tile.getEdge("pos-x", None).data,
                      "c": tile.getEdge("neg-y", None).data,
                      "d": tile.getEdge("neg-x", None).data}

    def test_rotate_one(self):
        """
        1 - Rotate edge labels 90 degrees
        """
        tile, labels = self.setup_tile()
        transformation = Transformation(tile.getEdgeLabels(None))
        rotation = transformation.rotate(Rotation.one)

        self.assertTrue(
            (rotation.xAxis == [labels["c"], labels["a"]]) and (rotation.yAxis == [labels["b"], labels["d"]]),
            msg=f"{rotation.xAxis=}, {rotation.yAxis=}"
        )

    def test_rotate_two(self):
        """
        2 - Rotate edge labels 180 degrees
        """
        tile, labels = self.setup_tile()
        transformation = Transformation(tile.getEdgeLabels(None))
        rotation = transformation.rotate(Rotation.two)

        self.assertTrue(
            (rotation.xAxis == [labels["b"], labels["d"]]) and (rotation.yAxis == [labels["a"], labels["c"]]),
            msg=f"{rotation.xAxis=}, {rotation.yAxis=}"
        )

    def test_rotate_three(self):
        """
        3 - Rotate edge labels 270 degrees
        """
        tile, labels = self.setup_tile()
        transformation = Transformation(tile.getEdgeLabels(None))
        rotation = transformation.rotate(Rotation.three)

        self.assertTrue(
            (rotation.xAxis == [labels["a"], labels["c"]]) and (rotation.yAxis == [labels["d"], labels["b"]]),
            msg=f"{rotation.xAxis=}, {rotation.yAxis=}"
        )

    def test_reflect_x(self):
        """
        4 - Reflects edge labels along the x-axis
        """
        tile, labels = self.setup_tile()
        transformation = Transformation(tile.getEdgeLabels(None))
        reflect = transformation.reflect(Axis.X)

        self.assertTrue(
            (reflect.xAxis == [labels["d"][::-1], labels["b"][::-1]]) and
            (reflect.yAxis == [labels["a"][::-1], labels["c"][::-1]]),
            msg=f"{reflect.xAxis=}, {reflect.yAxis=}"
        )

    def test_reflect_y(self):
        """
        5 - Reflects edge labels along the y-axis
        """
        tile, labels = self.setup_tile()
        transformation = Transformation(tile.getEdgeLabels(None))
        reflect = transformation.reflect(Axis.Y)

        self.assertTrue(
            (reflect.xAxis == [labels["b"][::-1], labels["d"][::-1]]) and
            (reflect.yAxis == [labels["c"][::-1], labels["a"][::-1]]),
            msg=f"{reflect.xAxis=}, {reflect.yAxis=}"
        )

    def test_rotate_invalid(self):
        """
        6 - Invalid rotation argument
        """
        tile, labels = self.setup_tile()
        transformation = Transformation(tile.getEdgeLabels(None))
        rotate = transformation.rotate("one")

        self.assertFalse(rotate.loaded)

    def test_reflect_invalid(self):
        """
        7 - Invalid reflection argument
        """
        tile, labels = self.setup_tile()
        transformation = Transformation(tile.getEdgeLabels(None))
        rotate = transformation.reflect("x")

        self.assertFalse(rotate.loaded)


if __name__ == '__main__':
    unittest.main()
