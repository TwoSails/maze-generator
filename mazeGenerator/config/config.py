"""
File: config.py
Date Created: 31/10/22
Description: This is reference to load in the configuration file which has
default program parameters such as the path which the tiles are located
"""

import json


class Config:
    def __init__(self) -> None:
        self.loadedConfig = False
        self.__configPath: str = "mazeGenerator/config/config.json"
        self.__configValues = []
        self.loadConfig()

    def loadConfig(self):
        """
        This method loads the configuration file,
        and sets the keys as attributes for dot notation access
        :return:
        """
        try:
            with open(self.__configPath, 'r') as file:
                content = json.load(file)
                for key in content.keys():
                    setattr(self, key, content[key])
                    self.__configValues.append(key)
                self.loadedConfig = True
        except FileNotFoundError:
            pass

    def saveConfig(self):
        config = {}
        for key in self.__configValues:
            config[key] = getattr(self, key)

        with open(self.__configPath, "w") as file:
            json.dump(config, file, indent=4)

    def get(self, key: str) -> any:
        """
        Fetching method for parameters
        :param key: identifier for value being fetched
        :return: attribute fetched
        """
        if key in self.__configValues:
            return getattr(self, key)
        else:
            return None

    def set(self, key: str, value, save: bool = False) -> bool:
        """
        Setter method for attributes in the config
        :param key: identifier for value being updated/set
        :param value: data being saved into the attribute
        :param save: boolean to check if config file should be updated
        :return: Success or Fail
        """
        if not isinstance(key, str):
            return False

        setattr(self, key, value)

        if key not in self.__configValues:
            self.__configValues.append(key)

        if save:
            self.saveConfig()

        return True
