from tkinter import Frame
from tkinter import Canvas as TkinterCanvas

from PIL import ImageTk, Image
from typing import Dict, Tuple, List

from ui.misc import NoneTypeCheck
from ui.Components import Component


class Canvas(Component):
    def __init__(self, parent: Frame, style: Dict, geometry: Tuple[int] | List[int]):
        super().__init__(parent, style, geometry)
        self.setComponent()
        self.data = NoneTypeCheck(style.get("data"), None)
        self.pixelsArr = []
        self.resolution = NoneTypeCheck(style.get("resolution"), [0, 0])
        if self.data is not None and self.resolution > 0:
            self.drawImage(resolutionX=self.resolution[0], resolutionY=self.resolution[1], data=self.data)
        self.image = None
        self.command = NoneTypeCheck(style.get("command"), None)
        if self.command is not None:
            self.component.bind("<Button-1>", self.command)
        self.ratio = 0
        self.generationImages = []

    def setComponent(self):
        self.component: TkinterCanvas = TkinterCanvas(self.componentFrame,
                                                      height=self.getAbsoluteHeight(),
                                                      width=self.getAbsoluteWidth(),
                                                      highlightbackground=self.backgroundColour,
                                                      highlightthickness=0)

    def clearCanvas(self):
        self.component.delete("all")

    def pixel(self, row: int, col: int, resolutionX: int, resolutionY: int, colour: str):
        """
        Draws a single pixel square on canvas
        :param row: row
        :param col: col
        :param resolutionX: x-axis resolution
        :param resolutionY: y-axis resolution
        :param colour: hex colour string
        """
        if len(colour) != 6:
            return
        scaleX = int(self.getAbsoluteWidth() / max(resolutionX, resolutionY))
        scaleY = int(self.getAbsoluteHeight() / max(resolutionX, resolutionY))
        self.component.create_rectangle(row * scaleX, col * scaleY,
                                        row * scaleX + scaleX, col * scaleY + scaleY,
                                        fill=f"#{colour.strip('#')}")
        self.component.update()

    def drawImage(self, resolutionX: int, resolutionY: int, data: str):
        """
        Pixel drawing of an image
        :param resolutionX: pixel count in x-axis
        :param resolutionY: pixel count in y-axis
        :param data: string of hex values corresponding to pixel
        """
        self.pixelsArr = []
        self.resolution = [resolutionX, resolutionY]
        for index in range(resolutionX * resolutionY):
            colour = data[index * 6: index * 6 + 6]
            self.pixelsArr.append(colour)
            self.pixel(row=index % resolutionY,
                       col=index // resolutionX,
                       resolutionX=resolutionX,
                       resolutionY=resolutionY,
                       colour=colour)

    def displayImage(self, filePath):
        """
        Places an image on the canvas
        :param filePath: Path to image
        """
        width = self.getAbsoluteWidth()
        img = Image.open(filePath)
        self.ratio = (img.size[0] / img.size[1])
        self.component.configure(width=width)
        img = img.resize((int(width if self.ratio > 1 else width * self.ratio),
                          int(self.getAbsoluteHeight() if self.ratio < 1 else self.getAbsoluteHeight() / self.ratio)),
                         Image.NEAREST)
        self.image = ImageTk.PhotoImage(img)
        self.component.create_image(self.getAbsoluteWidth() / 2, self.getAbsoluteHeight() / 2, image=self.image)

    def displayQuarterImage(self, filePath, quarter: int):
        """
        Displays an image in a quarter of the canvas area
        :param filePath: path to image
        :param quarter: 0 to 3 which quarter of canvas
        """
        img = Image.open(filePath)
        ratio = (img.size[0] / img.size[1])
        col = 3 if quarter // 2 == 1 else 1
        row = 3 if quarter % 2 == 1 else 1
        width = self.getAbsoluteWidth() / 2
        height = self.getAbsoluteHeight() / 2
        img = img.resize((int(width if ratio > 1 else width * ratio),
                          int(height if ratio < 1 else height / ratio)),
                         Image.NEAREST)
        if len(self.generationImages) > quarter:
            self.generationImages[quarter] = ImageTk.PhotoImage(img)
        else:
            self.generationImages.append(ImageTk.PhotoImage(img))
        self.component.create_image(self.getAbsoluteWidth() / 4 * row,
                                    self.getAbsoluteHeight() / 4 * col,
                                    image=self.generationImages[quarter])
        self.component.create_line(width, 0,
                                   width, self.getAbsoluteHeight(),
                                   fill="orange")
        self.component.create_line(0, height,
                                   self.getAbsoluteWidth(), height,
                                   fill="orange")

    def updateImage(self, resolutionX: int, resolutionY: int, data: str):  # Canvas efficiency
        if [resolutionX, resolutionY] != self.resolution:  # Different resolutions will be different pixel locations
            self.drawImage(resolutionX=resolutionX, resolutionY=resolutionY, data=data)
            return

        for index in range(resolutionX * resolutionY):
            colour = data[index * 6: index * 6 + 6]
            if colour != self.pixelsArr[index]:
                row = index % resolutionY
                col = index // resolutionX
                self.component.delete(f"{row}-{col}")  # Prevent overlapping which may hinder performance
                self.pixel(row=row,
                           col=col,
                           resolutionX=resolutionX,
                           resolutionY=resolutionY,
                           colour=colour)

    def drawRect(self, x1, y1, x2, y2, *_):
        self.component.create_rectangle(x1, y1, x2, y2, outline="#B7F42B", width=2)
