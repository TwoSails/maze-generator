"""
File: main.py
Date Created: 31/10/22
Description: This is the main entry point into the program.
This is required to be in the top level directory due to python file hierarchy and relative imports
"""

from mazeGenerator.mazeGenerator import App
from mazeGenerator.controllers import ImageHandler

app = App()
res = app.loadTileSet("default")
app.transformTileSet()
app.setupBoard(20, 20)
seed = app.board.seed

print(f"{seed=}")

resApp = app.run()
img = ImageHandler(width=app.board.width, height=app.board.height,
                   tileImageResolution=3, tileResolution=3,
                   board=resApp.data, tileSetName="default", seed=seed)
img.SetTiles(app.tileSet)
img.GenerateImage()
img.Scale(20)

