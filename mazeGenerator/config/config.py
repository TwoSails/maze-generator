"""
File: config.py
Date Created: 31/10/22
Description: This is reference to load in the configuration file which has default program parameters such as the path which the tiles are located
"""

import json


class Config:
    def __init__(self) -> None:
        self.loadedConfig = False
        self.__configPath: str = "mazeGenerator/config/config.json"
        self.loadConfig()

    def loadConfig(self):
        try:
            with open(self.__configPath, 'r') as file:
                content = json.load(file)
                for key in content.keys():
                    setattr(self, key, content[key])
                self.loadedConfig = True
        except FileNotFoundError:
            pass
