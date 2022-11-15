import unittest

from mazeGenerator.models import Edge


class TestEdge(unittest.TestCase):
    def test_symmetrical_data_types(self):
        """
        1 - Tests edge labels with symmetrical data types
        """
        edge = Edge("a", "b", "c", "d")
        self.assertTrue(
            (edge.positiveX() == "a") and
            (edge.positiveY() == "b") and
            (edge.negativeX() == "c") and
            (edge.negativeY() == "d")
        )

    def test_asymmetrical_data_types(self):
        """
        2 - Tests edge labels with symmetrical data types
        """
        edge = Edge("a", 2, "c", False)
        self.assertTrue(
            (edge.positiveX() == "a") and
            (edge.positiveY() == "") and
            (edge.negativeX() == "c") and
            (edge.negativeY() == "")
        )

    def test_positive_x(self):
        """
        3 - Tests +X label set correctly
        """
        edge = Edge("a", "b", "c", "d")
        self.assertEqual(edge.positiveX(), "a")

    def test_positive_y(self):
        """
        4 - Tests +Y label set correctly
        """
        edge = Edge("a", "b", "c", "d")
        self.assertEqual(edge.positiveY(), "b")

    def test_negative_x(self):
        """
        5 - Tests -X label set correctly
        """
        edge = Edge("a", "b", "c", "d")
        self.assertEqual(edge.negativeX(), "c")

    def test_negative_y(self):
        """
        6 - Tests -Y label set correctly
        """
        edge = Edge("a", "b", "c", "d")
        self.assertEqual(edge.negativeY(), "d")

    def test_get_invalid(self):
        """
        7 - Fetch positive X after not set correctly
        """
        edge = Edge(False, False, False, False)
        self.assertEqual(edge.positiveX(), "")
