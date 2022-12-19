"""
File: main.py
Date Created: 31/10/22
Description: This is the main entry point into the program.
This is required to be in the top level directory due to python file hierarchy and relative imports
"""
import time

from mazeGenerator.mazeGenerator import App
from mazeGenerator.controllers import ImageHandler

from tests.benchmark import execute_benchmark


def main():
    app = App()
    app.loadTileSet("default")
    app.transformTileSet()
    app.setupBoard(50, 50, "8143848079")
    seed = app.board.seed

    print(f"{seed=}")

    resApp = app.run()
    img = ImageHandler(width=app.board.width, height=app.board.height,
                       tileImageResolution=3, tileResolution=3,
                       board=resApp.data, tileSetName="default", seed=seed)
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

if __name__ == "__main__":
    # execute_benchmark("results/benchmark_12:54:36-17-Dec-2022.csv")
    start_time = time.perf_counter()
    main()
    # test(1)
    print(f"executed in {time.perf_counter() - start_time}s")
