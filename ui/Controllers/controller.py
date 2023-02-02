import threading
import logging
from PIL import Image, ImageTk

from typing import List

from mazeGenerator import App
from mazeGenerator.controllers import ImageHandler
from mazeGenerator.config import Config
from ui.Components import Canvas


logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.WARN,
                    datefmt="%H:%M:%S")


class Controller:
    def __init__(self):
        self.apps: List[App] = []
        self.inputData = {}
        self.config = Config()
        self.fetch = {"RuntimeBool": False,
                      "SeedBool": False,
                      "LogBool": False,
                      "SeedStr": "",
                      "WidthInt": 0,
                      "HeightInt": 0,
                      "GenerationsInt": 0}
        self.tileSet = "default"
        self.components = {}
        self.img = None

    def addComponent(self, tag, component):
        self.components[tag] = component
        if tag in self.fetch.keys():
            self.inputData[tag] = component.fetchData

    def convertBoardToCanvas(self, maze):
        outputDir = self.config.get("outputImgPath")
        filePath = f"{outputDir}maze_{maze}.png"
        img = Image.open(filePath)
        data = ""
        for pixel in img.getdata():
            data += f"{str(hex(pixel[0]))[2:].rjust(2, '0')}{str(hex(pixel[1]))[2:].rjust(2, '0')}{str(hex(pixel[2]))[2:].rjust(2, '0')}"

        canvas = self.getCanvas()
        if not canvas:
            return
        canvas.updateImage(resolutionX=img.size[0], resolutionY=img.size[1], data=data)

    def getCanvas(self) -> Canvas | bool:
        if "Canvas" not in self.components.keys():
            return False
        return self.components["Canvas"]

    def drawBoard(self, maze):
        outputDir = self.config.get("outputImgPath")
        filePath = f"{outputDir}maze_{maze}.png"
        canvas = self.getCanvas()
        canvas.displayImage(filePath)

    def assign_fetch(self):
        pass

    def gather_data(self):
        for tag in self.inputData.keys():
            if tag in self.fetch.keys():
                self.fetch[tag] = self.inputData[tag]()

    def generateMaze(self, index):
        maze = self.apps[index]
        resApp = maze.run()
        img = ImageHandler(width=maze.board.width, height=maze.board.height,
                           tileImageResolution=maze.tileImageResolution, tileResolution=maze.tileResolution,
                           board=resApp.data, tileSetName=maze.tileSetName, seed=maze.board.seed, name=f"maze_{index}")
        img.SetTiles(maze.tileSet)
        img.GenerateImage()

    def generateMazes(self):
        threads = []
        for i, maze in enumerate(self.apps):
            logging.warning(f"Maze {i} started")
            thread = threading.Thread(target=self.generateMaze, args=(i, ))
            threads.append(thread)
            thread.start()

        for i, thread in enumerate(threads):
            thread.join()
            logging.warning(f"Maze {i} completed")
            self.drawBoard(i)

    def button_run(self):
        self.apps = []
        self.gather_data()
        for generation in range(self.fetch["GenerationsInt"]):
            self.apps.append(App())
            self.apps[-1].loadTileSet(self.tileSet)
            self.apps[-1].setupBoard(height=self.fetch["HeightInt"],
                                     width=self.fetch["WidthInt"],
                                     seed=self.fetch["SeedStr"])
            self.generateMazes()

    def button_downloadPDF(self):
        pass

    def button_downloadPNG(self):
        pass

    def button_pausePlay(self):
        pass
