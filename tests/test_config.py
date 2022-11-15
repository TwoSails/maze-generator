import unittest

from mazeGenerator.config import Config


class TestConfig(unittest.TestCase):
    def test_load_file(self):
        """
        (1) Tests that the config file is loaded
        """

        config: Config = Config()
        self.assertTrue(config.loadedConfig)

    def test_get_valid_attribute(self):
        """
        (2) Tests that attributes can be fetched from config file
        :return:
        """

        config: Config = Config()
        self.assertNotEqual(config.get("dataPath"), None)

    def test_get_invalid_attribute(self):
        """
        (3) Tests that no fatal error occurs when fetching invalid attribute from config file
        :return:
        """
        config: Config = Config()
        self.assertEqual(config.get("pineapplesOnPizza"), None)

    def test_get_int_attribute(self):
        """
        (4) Tests that no fatal error occurs when fetching integer attribute from config file
        :return:
        """
        config: Config = Config()
        self.assertEqual(config.get(1), None)

    def test_set_valid_attribute(self):
        """
        (5) Tests that value can be set and saved
        :return:
        """
        config: Config = Config()
        key = "alpha"
        value = "beta"
        config.set(key, value)
        self.assertEqual(config.get(key), value)

    def test_set_invalid_attribute(self):
        """
        (6) Tests that no fatal error occurs when setting invalid attribute
        :return:
        """
        config: Config = Config()
        key = 1
        value = "beta"
        self.assertFalse(config.set(key, value))
        self.assertEqual(config.get(key), None)

    def test_set_valid_save_attribute(self):
        """
        (7) Tests that value can be set and saved in config file
        :return:
        """
        config: Config = Config()
        key = "alpha"
        value = "beta"
        self.assertTrue(config.set(key, value, True))
        self.assertEqual(config.get(key), value)

    def test_set_invalid_save_attribute(self):
        """
        (8) Tests that no fatal error occurs when setting invalid attribute and trying to save
        :return:
        """
        config: Config = Config()
        key = 1
        value = "beta"
        self.assertFalse(config.set(key, value, True))
        self.assertEqual(config.get(key), None)


if __name__ == "__main__":
    unittest.main()
