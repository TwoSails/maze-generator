"""
File: imageHandler.py
Created: 9/12/22
Description: This is the controller for exporting mazes
"""
# Local Imports
from mazeGenerator.models import Cell, Tile
from mazeGenerator.data import Axis, Rotation
from mazeGenerator.config import Config

from mazeGenerator.response import Response, Ok, Err, ExceedsBounds

# Python Imports
from typing import List

# External Packages
from PIL import Image as ImageFuncs
from PIL import ImageDraw, PngImagePlugin
from PIL.Image import Image


class ImageHandler:
    def __init__(self, width: int = -1, height: int = -1, tileImageResolution: int = -1, tileResolution: int = -1,
                 tileSet: List[Tile] = None, board: List[Cell] = None, tileSetName: str = "", name: str = "",
                 seed: str = ""):
        """
        :param width: Number of cells in the horizontal
        :param height: Number of cells in the vertical
        :param tileImageResolution: Pixel resolution of the tile image
        :param tileResolution: Edge label resolution of the tiles
        :param tileSet: List of tiles used in the board
        :param board: List of cells
        :param tileSetName: Name of the tile set used
        :param name: Name of the image output
        :param seed: The boards seed for generation
        """
        if tileSet is None:
            tileSet = []
        if board is None:
            board = []
        self.config: Config = Config()
        self.tileSet: List[Tile] = tileSet
        self.tileSetName: str = tileSetName
        self.tileLog: dict = {}
        self.board: List[Cell] = board
        self.width: int = width
        self.height: int = height
        self.tileImageResolution: int = tileImageResolution
        self.name: str = name
        self.tileResolution: int = tileResolution
        self.maze: Image | None = None
        self.seed: str = seed

    @staticmethod
    def ValidateMultiTypeInputToInteger(validate, bound: int = 0) -> Response:
        if isinstance(validate, str):
            try:
                validate = int(validate)
            except ValueError:
                return Err(TypeError)

        validate = abs(validate)  # Converts to positive value
        if validate <= bound:
            return Err()

        return Ok(validate)

    def SetTiles(self, tiles: List[Tile]) -> Response:
        for tile in tiles:
            if not isinstance(tile, Tile):
                return Err(TypeError)
        self.tileSet = tiles

        for tile in self.tileSet:
            if tile.getImage() is None:
                tile.loadImage()
            tileName = tile.getName()
            self.tileLog[tileName] = {
                "base": tile.getImage()
            }
            for transformation in [Rotation.one, Rotation.two, Rotation.three, Axis.X, Axis.Y]:
                self.tileLog[tileName][transformation] = self.TransformTileImage(transformation, tile)

        return Ok()

    def SetWidth(self, width: int) -> Response:
        validate = self.ValidateMultiTypeInputToInteger(width)
        if validate.success:
            self.width = validate.data

        return validate

    def SetHeight(self, height: int) -> Response:
        validate = self.ValidateMultiTypeInputToInteger(height)
        if validate.success:
            self.height = validate.data

        return validate

    def SetTileImageResolution(self, res: int) -> Response:
        validate = self.ValidateMultiTypeInputToInteger(res)
        if validate.success:
            self.tileImageResolution = validate.data

        return validate

    def SetSeed(self, seed) -> Response:
        self.seed = str(seed)
        return Ok()

    def GetIdx(self, row: int, col: int) -> Response:
        if row > self.height or col > self.width or row < 0 or col < 0:
            return Err(ExceedsBounds)

        return Ok(row * self.width + col)

    def GenerateBlankImage(self) -> Response:
        if self.width <= 0 or self.tileImageResolution <= 0 or self.height <= 0:
            return Err(ExceedsBounds)
        self.maze = ImageFuncs.new("RGBA",
                                   (self.width * self.tileImageResolution, self.height * self.tileImageResolution))

        return Ok()

    def PlaceCell(self, row: int, col: int) -> Response:
        cornerCoords = (col * self.tileImageResolution, row * self.tileImageResolution)
        idx = self.GetIdx(row, col)
        if not idx.success:
            return idx

        if idx.data >= len(self.board) or idx.data < 0:
            return Err(ExceedsBounds)

        cell = self.board[idx.data]
        if cell.collapsed:
            img = self.tileLog[cell.tile.getName()][cell.transformation if cell.transformation is not None else "base"]
        else:
            img = ImageFuncs.new("RGBA", (self.tileImageResolution, self.tileImageResolution), color="#555555")
        for xy, pixel in enumerate(list(img.getdata())):
            rel_x = xy % self.tileImageResolution
            rel_y = xy // self.tileImageResolution
            self.maze.putpixel((cornerCoords[0] + rel_x, cornerCoords[1] + rel_y), pixel)

        return Ok()

    @staticmethod
    def TransformTileImage(transformation: Axis | Rotation, image: Tile):
        img = image.getImage()
        if img is None:
            image.loadImage()
            img = image.getImage()
        match transformation:
            case Rotation.one:
                img = img.transpose(ImageFuncs.Transpose.ROTATE_90)
            case Rotation.two:
                img = img.transpose(ImageFuncs.Transpose.ROTATE_180)
            case Rotation.three:
                img = img.transpose(ImageFuncs.Transpose.ROTATE_270)
            case Axis.X:
                img = img.transpose(ImageFuncs.Transpose.FLIP_TOP_BOTTOM)
            case Axis.Y:
                img = img.transpose(ImageFuncs.Transpose.FLIP_LEFT_RIGHT)
            case _:
                img = None

        return img

    def SaveImage(self):
        outputDir = self.config.get("outputImgPath")
        filePath = f"{outputDir}{self.name if self.name != '' else self.tileSetName}.png"
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("maze-seed", f"{self.seed}")
        try:
            self.maze.save(filePath, pnginfo=metadata)
        except ValueError:
            return Err(ValueError)
        except OSError:
            return Err(OSError)

        return Ok()

    def GenerateImage(self):
        self.GenerateBlankImage()
        for cell in self.board:
            self.PlaceCell(cell.row, cell.col)
        # self.CalculateAverageColour()
        return self.SaveImage()

    def CalculateAverageColour(self):
        palettes = []
        for tile in self.tileSet:
            img = tile.getImage()
            if img is None:
                continue

            AVG = [0, 0, 0]
            pixels = img.getdata()
            for pixel in pixels:
                AVG[0] += pixel[0]
                AVG[1] += pixel[1]
                AVG[2] += pixel[2]

            print(sum(AVG) / len(pixels))

        print(f"{palettes=}")

    def Scale(self, scale=2):
        """
        Scales the image from absolute size to larger resolution
        """
        scaled_img = ImageFuncs.new("RGBA", (self.maze.width * scale, self.maze.height * scale))
        draw = ImageDraw.Draw(scaled_img)
        for xy, pixel in enumerate(list(self.maze.getdata())):
            x = xy % self.maze.width
            y = xy // self.maze.height
            draw.rectangle((x * scale, y * scale, x * scale + scale, y * scale + scale), fill=pixel, outline=None)
        outputDir = self.config.get("outputImgPath")
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("maze-seed", f"{self.seed}")
        scaled_img.save(f"{outputDir}{self.name if self.name != '' else self.tileSetName}_scaled.png", pnginfo=metadata)
