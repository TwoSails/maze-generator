import unittest

from mazeGenerator.config import Config


class TestConfig(unittest.TestCase):
    def test_load_file(self):
        """
        Tests that the config file is loaded
        """

        config: Config = Config()
        self.assertTrue(config.loadedConfig)


if __name__ == "__main__":
    unittest.main()