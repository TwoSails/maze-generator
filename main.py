"""
File: main.py
Date Created: 31/10/22
Description: This is the main entry point into the program.
This is required to be in the top level directory due to python file hierarchy and relative imports
"""
import time

from mazeGenerator.mazeGenerator import App
from mazeGenerator.controllers import ImageHandler

from ui.view import View

from tests.benchmark import execute_benchmark


def main():
    app = App()
    app.loadTileSet("circuit", False)
    app.setupBoard(5, 5)  # seed= "8143848079"
    seed = app.board.seed

    print(f"{seed=}")

    print(f"{app.tileSet=}")

    resApp = app.run()
    print(f"{resApp.success=}")
    img = ImageHandler(width=app.board.width, height=app.board.height,
                       tileImageResolution=app.tileImageResolution, tileResolution=app.tileResolution,
                       board=resApp.data, tileSetName=app.tileSetName, seed=seed)
    img.SetTiles(app.tileSet)
    img.GenerateImage()
    img.Scale(20)

def test(b):
    s_time = time.perf_counter()
    if abs(b) > 0:
        a = 0
    print(f"executed in {time.perf_counter() - s_time}")
    s_time = time.perf_counter()
    if -b < 0 or b > 0:
        a = 0
    print(f"executed in {time.perf_counter() - s_time}")


def gui():
    ui = View()
    ui.displayWindow("main")
    ui.mainloop()


if __name__ == "__main__":
    # execute_benchmark("results/benchmark_12:54:36-17-Dec-2022.csv")
    # start_time = time.perf_counter()
    gui()
    # test(1)
    # print(f"executed in {time.perf_counter() - start_time}s")
