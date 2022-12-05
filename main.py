"""
File: main.py
Date Created: 31/10/22
Description: This is the main entry point into the program.
This is required to be in the top level directory due to python file hierarchy and relative imports
"""

from mazeGenerator.mazeGenerator import App

app = App()
res = app.loadTileSet("default")
print(res.success)
app.transformTileSet()
app.setupBoard(5, 5)

app.run()
