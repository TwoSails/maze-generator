import unittest
from mazeGenerator.response import Ok, Err, Response


class TestResponse(unittest.TestCase):
    def test_ok(self):
        self.assertTrue(Ok("Hello").success)

    def test_err(self):
        self.assertFalse(Err(IndexError).success)

    def test_empty_ok(self):
        self.assertTrue(Ok().success)

    def test_empty_err(self):
        self.assertFalse(Err().success)


if __name__ == '__main__':
    unittest.main()
