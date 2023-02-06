import time
from tkinter.filedialog import asksaveasfile
import threading
import logging
from io import BytesIO
from PIL import Image as PillowImage
from typing import List

from mazeGenerator import App
from mazeGenerator.controllers import ImageHandler
from mazeGenerator.config import Config
from ui.Components import Canvas


logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.WARN,
                    datefmt="%H:%M:%S")


class Controller:
    def __init__(self, window=None):
        self.windowManager = window
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
        self.speed = 2
        self.currentFrame = 0
        self.play = False
        self.currentGeneration = 0

    def addComponent(self, tag, component):
        self.components[tag] = component
        if tag in self.fetch.keys():
            self.inputData[tag] = component.fetchData

    def convertBoardToCanvas(self, maze):
        outputDir = self.config.get("outputImgPath")
        filePath = f"{outputDir}maze_{maze}.png"
        img = PillowImage.open(filePath)
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
        self.img = f"{outputDir}maze_{maze}.png"
        canvas = self.getCanvas()
        canvas.displayImage(self.img)

    def assign_fetch(self):
        pass

    def gather_data(self):
        for tag in self.inputData.keys():
            if tag in self.fetch.keys():
                self.fetch[tag] = self.inputData[tag]()

    def generateFrame(self, board, boardIdx, index):
        maze = self.apps[index]
        img = ImageHandler(width=maze.board.width, height=maze.board.height,
                           tileImageResolution=maze.tileImageResolution, tileResolution=maze.tileResolution,
                           board=board, tileSetName=maze.tileSetName, seed=maze.board.seed, name=f"frames/maze_{boardIdx}")
        img.SetTiles(maze.tileSet)
        img.GenerateImage()

    def generateAnimation(self, index):
        threads = []
        for boardIdx, board in enumerate(self.apps[index].board.log):
            thread = threading.Thread(target=self.generateFrame, args=(board, boardIdx, index, ))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def displayAnimation(self, index):
        canvas = self.getCanvas()
        progressBar = self.components["AnimationProgressBar"]
        progressText = self.components["AnimationProgressText"]
        if not canvas:
            return
        outputDir = f"{self.config.get('outputImgPath')}frames/maze_"
        length = len(self.apps[index].board.log)
        while self.currentFrame < length and self.play:
            canvas.displayImage(outputDir + f"{self.currentFrame}.png")
            canvas.component.update()
            self.currentFrame += 1
            progress = int(self.currentFrame/length * 100)
            progressBar.set(progress)
            progressText.update(f"{progress}%")
            time.sleep(0.2 / self.speed)

    def generateMaze(self, index):
        maze = self.apps[index]
        if maze.board.width * maze.board.height > 600 or self.fetch["GenerationsInt"] > 1:
            self.fetch["LogBool"] = False
        resApp = maze.run(self.fetch["LogBool"])
        img = ImageHandler(width=maze.board.width, height=maze.board.height,
                           tileImageResolution=maze.tileImageResolution, tileResolution=maze.tileResolution,
                           board=resApp.data, tileSetName=maze.tileSetName, seed=maze.board.seed, name=f"maze_{index}")
        img.SetTiles(maze.tileSet)
        img.GenerateImage()

    def setSeed(self, seed):
        if "SeedOut" not in self.components.keys():
            return

        seedComponent = self.components["SeedOut"]
        seedComponent.update(f"Seed: {seed}")

    def removeSeed(self):
        if "SeedOut" not in self.components.keys():
            return

        seedComponent = self.components["SeedOut"]
        seedComponent.update("")

    def setRuntime(self, time):
        if "RuntimeOut" not in self.components.keys():
            return

        runtimeComponent = self.components["RuntimeOut"]
        runtimeComponent.update(f"Runtime: {round(time, 5)}s")

    def removeRuntime(self):
        if "RuntimeOut" not in self.components.keys():
            return

        runtimeComponent = self.components["RuntimeOut"]
        runtimeComponent.update("")

    def displayTiles(self, tiles):
        abcTiles = filter(lambda i: False if i is None else "abc" in i, list(self.components.keys()))
        abcTiles = list(abcTiles)
        overflow = 0

        for idx, tile in enumerate(tiles.keys()):
            if idx >= len(abcTiles) - 1:
                overflow += int(tiles[tile])
                continue
            text = f"{tiles[tile]}x"
            filename = f"./data/{self.tileSet}/{tile}.png"
            component = self.components[f"abcTile{idx + 1}"]
            component.update(text, filename)

        for tile in range(len(tiles.keys()) + 1, len(abcTiles)):
            self.components[f"abcTile{tile}"].update()

        if overflow > 0:
            self.components["abcTileOverflow"].update(text=f"{overflow}x", filename=f"./data/{self.tileSet}/icon.png")
        else:
            self.components["abcTileOverflow"].update()

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
            if self.fetch["SeedBool"]:
                self.setSeed(self.apps[i].board.seed)
            else:
                self.removeSeed()
            if self.fetch["RuntimeBool"]:
                self.setRuntime(self.apps[i].runtime)
            else:
                self.removeRuntime()
            self.displayTiles(self.apps[i].countTiles())
            if self.fetch["LogBool"]:
                self.generateAnimation(i)
            self.currentGeneration = i

    def button_run(self):
        self.currentFrame = 0
        self.apps = []
        self.gather_data()
        for generation in range(self.fetch["GenerationsInt"]):
            self.apps.append(App())
            self.apps[-1].loadTileSet(self.tileSet)
            self.apps[-1].setupBoard(height=self.fetch["HeightInt"],
                                     width=self.fetch["WidthInt"],
                                     seed=self.fetch["SeedStr"])
            self.generateMazes()

    def button_downloadPDF(self, *_):
        file = asksaveasfile(mode="wb", defaultextension=".pdf")
        if file is None:
            return

        io = BytesIO()
        img = PillowImage.open(self.img).convert("RGB")
        img = img.resize((img.size[0] * 50, img.size[1] * 50), PillowImage.NEAREST)
        img.save(io, "PDF")
        img.seek(0)
        file.write(io.getbuffer())
        file.close()

    def button_downloadPNG(self, *_):
        file = asksaveasfile(mode="wb", defaultextension=".png")
        if file is None:
            return

        io = BytesIO()
        img = PillowImage.open(self.img)
        img = img.resize((img.size[0] * 100, img.size[1] * 100), PillowImage.NEAREST)
        img.save(io, "PNG")
        img.seek(0)
        file.write(io.getbuffer())
        file.close()

    def button_playPause(self, *_):
        self.play = not self.play
        button = self.components["PlayPauseButton"]
        button.update(filename=f"./ui/Config/data/{'pause' if self.play else 'play'}Button.png")
        if len(self.apps) == 0:
            return

        if self.currentFrame == len(self.apps[self.currentGeneration].board.log):
            self.currentFrame = 0

        if self.play:
            self.displayAnimation(self.currentGeneration)

    def canvas_select(self, pos):
        canvas = self.components["Canvas"]
        widthOfCells = canvas.getAbsoluteWidth() / self.apps[self.currentGeneration].board.width
        heightOfCells = canvas.getAbsoluteHeight() / self.apps[self.currentGeneration].board.height
        row = int(pos.y / heightOfCells)
        col = int(pos.x / widthOfCells)
        idx = row * self.apps[self.currentGeneration].board.width + col
        if self.fetch["LogBool"]:
            cell = self.apps[self.currentGeneration].board.log[self.currentFrame - 1][idx]
        else:
            cell = self.apps[self.currentGeneration].board.board[idx]
        print(cell)

    def progress_speed(self, pos):
        control = self.components["AnimationSpeedControl"]
        percentage = pos.x / control.getAbsoluteWidth()
        percentage = int(percentage * 100)
        control.set(percentage)
        self.speed = percentage / 25
