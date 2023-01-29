from tkinter import Frame
from tkinter import Canvas as TkinterCanvas

from typing import Dict, Tuple, List

from ui.misc import NoneTypeCheck
from ui.Components import Component


class Canvas(Component):
    def __init__(self, parent: Frame, style: Dict, geometry: Tuple[int] | List[int]):
        super().__init__(parent, style, geometry)
        self.component: TkinterCanvas = TkinterCanvas(self.componentFrame,
                                                      height=self.getAbsoluteHeight(),
                                                      width=self.getAbsoluteWidth(),
                                                      highlightbackground=self.backgroundColour,
                                                      highlightthickness=0)
        self.data = NoneTypeCheck(style.get("data"), None)
        self.pixelsArr = []
        self.resolution = NoneTypeCheck(style.get("resolution"), 0)
        if self.data is not None and self.resolution > 0:
            self.drawImage(self.resolution, self.data)

    def clearCanvas(self):
        self.component.delete("all")

    def pixel(self, row: int, col: int, resolution: int, colour: str):
        scaleX = self.getAbsoluteWidth() / resolution
        scaleY = self.getAbsoluteHeight() / resolution
        self.component.create_rectangle(row * scaleX, col * scaleY,
                                        row * scaleX + scaleX, col * scaleY + scaleY,
                                        tags=f"{row}-{col}",
                                        fill=f"#{colour.strip('#')}")

    def drawImage(self, resolution: int, data: str):
        self.pixelsArr = []
        self.resolution = resolution
        for index in range(resolution ** 2):
            colour = data[index * 6: index * 6 + 6]
            self.pixelsArr.append(colour)
            self.pixel(row=index // resolution,
                       col=index % resolution,
                       resolution=resolution,
                       colour=colour)

    def updateImage(self, resolution: int, data: str):  # Canvas efficiency
        if resolution != self.resolution:  # Totally different therefore indexes of pixels wouldn't match
            self.drawImage(resolution, data)
            return

        for index in range(resolution ** 2):
            colour = data[index * 6: index * 6 + 6]
            if colour != self.pixelsArr[index]:
                row = index // resolution
                col = index % resolution
                self.component.delete(f"{row}-{col}")  # Prevent overlapping which may hinder performance
                self.pixel(row=row,
                           col=col,
                           resolution=resolution,
                           colour=colour)
