import time

from mazeGenerator import App
from mazeGenerator.controllers import ImageHandler

import logging

logging.basicConfig(level=logging.INFO)


def main(width, height, seed=0):
    app = App()
    app.loadTileSet("default")
    app.transformTileSet()
    app.setupBoard(width, height, seed)
    seed = app.board.seed

    resApp = app.run()
    success = resApp.success
    #  img = ImageHandler(width=app.board.width, height=app.board.height,
    #                     tileImageResolution=3, tileResolution=3,
    #                     board=resApp.data, tileSetName="default", seed=seed)
    #  img.SetTiles(app.tileSet)
    #  img.GenerateImage()
    #  img.Scale(20)
    return seed, success


def save_data(data):
    with open(f"results/benchmark_{time.strftime('%H:%M:%S-%d-%h-%Y')}.csv", "w") as file:
        file.writelines(data)


def load_seeds(benchmark):
    seeds = []
    with open(benchmark, "r") as file:
        line = file.readline()
        while line != "":
            line = line.split(",")
            seeds.append(line[4].strip())
            line = file.readline()

    return seeds


def execute_benchmark(benchmark=None):
    repetitions = 6
    test = 1
    data = []
    params = [(x, x) for x in range(5, 51, 5)]
    skipped = 0
    seeds = []
    test_start = time.perf_counter()
    if benchmark is not None:
        seeds = load_seeds(benchmark)
    for param in params:
        repetition = 1
        while repetition - 1 < repetitions:
            seedParam = 0 if benchmark is None else seeds[test - 1]
            start_time = time.perf_counter()
            seed, success = main(param[0], param[1], seedParam)
            if not success:
                logging.warning(f"{seed} not successful - skipping")
                skipped += 1
                continue
            end_time = time.perf_counter()
            duration = end_time - start_time
            logging.info(f"Test {test}: Executed {repetition} - {param} in {duration}s")
            data.append(f"{test}, {param[0]}, {param[1]}, {repetition}, {seed}, {success}, {duration}\n")
            repetition += 1
            test += 1

    save_data(data)
    logging.info(f"Tests complete\n{skipped} generations failed\n[Finished in {round(time.perf_counter() - test_start, 3)}s]")
