import os
import time
from tkinter.filedialog import asksaveasfile, askdirectory
from tkinter.messagebox import showerror
import threading
import logging
import shutil
from io import BytesIO
from PIL import Image as PillowImage
from typing import List
from pycallgraph2 import PyCallGraph
from pycallgraph2.output import GraphvizOutput

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
                      "WidthInt": 5,
                      "HeightInt": 5,
                      "GenerationsInt": 1,
                      "GraphBool": False}
        self.tileSet = "default"
        self.secondaryTileSet = "default"
        self.components = {}
        self.img = None
        self.speed = 2
        self.currentFrame = 0
        self.play = False
        self.played = False
        self.currentGeneration = None

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

    def displayGenerations(self):
        for i, generation in enumerate(self.apps):
            outputDir = self.config.get("outputImgPath")
            img = f"{outputDir}maze_{i}.png"
            canvas = self.components["Canvas"]
            canvas.displayQuarterImage(img, i)

    def generateFrame(self, board, boardIdx, index):
        """
        Frame handler
        :param board: <cells>
        :param boardIdx: position in sequence of maze creation
        :param index: generation of maze
        :return:
        """
        maze = self.apps[index]
        img = ImageHandler(width=maze.board.width, height=maze.board.height,
                           tileImageResolution=maze.tileImageResolution, tileResolution=maze.tileResolution,
                           board=board, tileSetName=maze.tileSetName, seed=maze.board.seed, name=f"frames/maze_{boardIdx}")
        img.SetTiles(maze.tileSet)
        img.GenerateImage()

    def generateAnimation(self, index):
        """
        Controller to distribute non-blocking frame generation of board states
        Has to be non-blocking due to large volume of I/O interactions
        :param index:
        :return:
        """
        threads = []
        for boardIdx, board in enumerate(self.apps[index].board.log):
            thread = threading.Thread(target=self.generateFrame, args=(board, boardIdx, index, ))
            threads.append(thread)
            thread.start()

    def displayAnimation(self, index, regen=False):
        """
        Display frames of maze generation in sequence at varying speed and with playback controls
        :param index:
        :param regen:
        :return:
        """
        canvas = self.getCanvas()
        progressBar = self.components["AnimationProgressBar"]
        progressText = self.components["AnimationProgressText"]
        if not canvas:
            return
        outputDir = f"{self.config.get('outputImgPath')}frames/maze_"
        length = len(self.apps[index].board.log)
        regenIncrement = regen
        while self.currentFrame < length and (self.play or regenIncrement):
            frame = self.currentFrame
            if regenIncrement and self.played:
                frame -= 1
            elif regenIncrement:
                frame = length - 1

            if frame < 0:
                frame = length - 1
            canvas.displayImage(outputDir + f"{frame}.png")
            canvas.component.update()
            if not regenIncrement:
                self.currentFrame += 1
            progress = int(self.currentFrame/length * 100)
            progressBar.set(progress)
            progressText.update(f"{progress}%")
            time.sleep(0.2 / self.speed)
            regenIncrement = False

    def generateMaze(self, index):
        """
        Handler method to generate a maze
        :param index:
        :return:
        """
        maze = self.apps[index]
        if maze.board.width * maze.board.height > 600:
            self.fetch["LogBool"] = False
        if self.fetch["GraphBool"] and maze.board.width * maze.board.height < 600:
            graphviz = GraphvizOutput()
            graphviz.output_file = "./ui/Config/data/maze_graph.png"
            with PyCallGraph(output=graphviz):
                resApp = maze.run(self.fetch["LogBool"])
        else:
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

    def setRuntime(self, runtime):
        if "RuntimeOut" not in self.components.keys():
            return

        runtimeComponent = self.components["RuntimeOut"]
        runtimeComponent.update(f"Runtime: {round(runtime, 5)}s")

    def removeRuntime(self):
        if "RuntimeOut" not in self.components.keys():
            return

        runtimeComponent = self.components["RuntimeOut"]
        runtimeComponent.update("")

    def displayTiles(self, tiles):
        """
        Shows tile count of tiles used in maze
        :param tiles: tile count
        :return:
        """
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

    def displayMaze(self, i, frame=False):
        """
        Method to render all information onto the board widget
        Used in window switching
        :param i: Generation of maze to display
        :param frame:
        :return:
        """
        if frame:
            self.displayAnimation(i, True)
        else:
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
            if self.fetch["GenerationsInt"] == 1:
                self.currentGeneration = 0
                self.displayMaze(i)

    def button_run(self):
        canvas = self.components["Canvas"]
        canvas.clearCanvas()
        self.currentFrame = 0
        self.currentGeneration = None
        self.played = False
        self.apps = []
        self.gather_data()
        for generation in range(self.fetch["GenerationsInt"]):
            self.apps.append(App())
            self.apps[generation].loadTileSet(self.tileSet)
            self.apps[generation].setupBoard(height=self.fetch["HeightInt"],
                                             width=self.fetch["WidthInt"],
                                             seed=self.fetch["SeedStr"])
            self.generateMazes()
        if self.fetch["GenerationsInt"] > 1:
            self.displayGenerations()

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
        self.played = True
        button = self.components["PlayPauseButton"]
        button.update(filename=f"./ui/Config/data/{'pause' if self.play else 'play'}Button.png")
        if len(self.apps) == 0:
            return

        if self.currentFrame == len(self.apps[self.currentGeneration].board.log):
            self.currentFrame = 0

        if self.play:
            self.displayAnimation(self.currentGeneration)

    def button_back(self, *_):
        self.windowManager.displayWindow("main")
        self.displayMaze(self.currentGeneration)
        self.displaySecondaryTileSet()

    def selectingGenerations(self, pos):
        canvas = self.components["Canvas"]
        width = canvas.getAbsoluteWidth()
        height = canvas.getAbsoluteHeight()
        if pos.x < width / 2:
            col = 0
        else:
            col = 1
        if pos.y < height / 2:
            row = 0
        else:
            row = 1
        self.currentGeneration = col + row * 2
        self.displayMaze(self.currentGeneration)

    def selectingCell(self, pos):
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
        grid = {
            "type": "Grid",
            "height": "0.25r",
            "width": "0.25r",
            "x": "0.05r",
            "y": 0,
            "column-padding": 15,
            "background-colour": "#333333",
            "elements": []
        }
        if not cell.collapsed:
            for tile in cell.availableTiles:
                grid["elements"].append({
                    "type": "Image",
                    "height": 30,
                    "width": 30,
                    "x": "0.05r",
                    "y": 0,
                    "filename": f"./data/{tile.getTileSet()}/{tile.getName()}.png",
                    "transformation": f"{tile.getTransformation()}",
                    "background-colour": "#333333"
                })
        rowElement = {
            "type": "Row",
            "x": "0.05r",
            "y": 550,
            "background-colour": "#333333",
            "contentLeft": None if cell.collapsed else grid,
            "contentRight": None
        }
        self.windowManager.displayWindow("cell", injectStyle=rowElement, injectWidget="Sidebar")
        self.displayMaze(self.currentGeneration, self.fetch["LogBool"])
        self.displayCell(cell)
        self.highlightCell(row, col)

    def canvas_select(self, pos):
        if len(self.apps) == 0:
            return
        if self.currentGeneration is None:
            self.selectingGenerations(pos)
        else:
            self.selectingCell(pos)

    def progress_speed(self, pos):
        control = self.components["AnimationSpeedControl"]
        percentage = pos.x / control.getAbsoluteWidth()
        percentage = int(percentage * 100)
        control.set(percentage)
        self.speed = percentage / 25

    def highlightCell(self, row, col):
        canvas = self.components["Canvas"]
        widthOfCells = canvas.getAbsoluteWidth() / self.apps[self.currentGeneration].board.width
        heightOfCells = canvas.getAbsoluteHeight() / self.apps[self.currentGeneration].board.height
        x1 = widthOfCells * col
        y1 = heightOfCells * row
        x2 = widthOfCells * (col + 1)
        y2 = heightOfCells * (row + 1)
        canvas.drawRect(x1, y1, x2, y2)

    def displayCell(self, cell):
        CellName = self.components["CellName"]
        CellTransformation = self.components["CellTransformation"]
        CellResolution = self.components["CellResolution"]
        if cell.collapsed:
            CellName.update(cell.getTile().getName())
            CellTransformation.update(cell.getTile().getTransformation())
            CellResolution.update(cell.getTile().getResolution())
        else:
            CellName.update("Uncollapsed")
            CellTransformation.update("Uncollapsed")
            CellResolution.update("Uncollapsed")
        CellLocation = self.components["CellLocation"]
        idx = cell.row * self.apps[self.currentGeneration].board.width + cell.col
        CellLocation.update(f"Row {cell.row} / Col {cell.col} - Index {idx}")
        CellEntropy = self.components["CellEntropy"]
        CellEntropy.update(cell.entropy)
        CellCollapsed = self.components["CellCollapsed"]
        CellCollapsed.update(f"{'True' if cell.collapsed else 'False'}")

    @staticmethod
    def isDirectoryTileSet(path) -> bool:
        print(path)
        contents = os.listdir(path)
        if "tiles.json" not in contents:
            return False
        return True
    
    def button_add_tileset(self, *_):
        configDataPath = os.path.abspath(self.config.get("dataPath"))
        directory = askdirectory()
        if directory == "":
            return
        if not self.isDirectoryTileSet(directory):
            showerror("Invalid Tile Set Folder", "Invalid Tile Set Folder\ntiles.json file is missing")
            return
        name = directory.split("/")[-1]
        if configDataPath not in directory:
            os.makedirs(f"{configDataPath}/{name}")
            for file in os.listdir(directory):
                if os.path.isdir(directory + file):
                    continue
                shutil.copy(f"{directory}/{file}", f"{configDataPath}/{name}/{file}")

        self.tileSet = name
        self.secondaryTileSet = name
        self.displaySecondaryTileSet()

    def displaySecondaryTileSet(self):
        secondaryTileSet = self.components["secondaryTileSet"]
        secondaryTileSet.update(filename=f"{self.config.get('dataPath')}{self.secondaryTileSet}/icon.png")
        self.tileSetSelection()

    def tileSetSelection(self):
        if self.tileSet == "default":
            self.components["primaryTileSet"].border("orange")
            self.components["secondaryTileSet"].border(None)
        else:
            self.components["primaryTileSet"].border(None)
            self.components["secondaryTileSet"].border("orange")

    def button_primaryTileSet(self, *_):
        self.tileSet = "default"
        self.tileSetSelection()

    def button_secondaryTileSet(self, *_):
        self.tileSet = self.secondaryTileSet
        self.tileSetSelection()

    def button_graph(self, *_):
        if not self.fetch["GraphBool"] or "maze_graph.png" not in os.listdir("./ui/Config/data"):
            return
        img = PillowImage.open("./ui/Config/data/maze_graph.png")
        img.show()

    def button_graph_save(self, *_):
        if not self.fetch["GraphBool"] or "maze_graph.png" not in os.listdir("./ui/Config/data"):
            return
        file = asksaveasfile(mode="wb", defaultextension=".png")
        if file is None:
            return

        io = BytesIO()
        img = PillowImage.open("./ui/Config/data/maze_graph.png")
        img.save(io, "PNG")
        img.seek(0)
        file.write(io.getbuffer())
        file.close()
