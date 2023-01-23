import json
from json import JSONDecodeError


class Config:
    def __init__(self) -> None:
        self.loadedConfig = False
        self.__configPath: str = "ui/Config/config.json"
        self.config = {}
        self.loadConfig()

    def loadConfig(self):
        """
        This method loads the configuration file
        :return:
        """
        try:
            with open(self.__configPath, 'r') as file:
                self.config = json.load(file)
                self.loadedConfig = True
        except FileNotFoundError or JSONDecodeError:
            pass
        except json.decoder.JSONDecodeError:
            raise Exception("Failed to load configuration - Invalid JSON Format")
