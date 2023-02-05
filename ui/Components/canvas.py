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

    def setComponent(self):
        self.component: TkinterCanvas = TkinterCanvas(self.componentFrame,
                                                      height=self.getAbsoluteHeight(),
                                                      width=self.getAbsoluteWidth(),
                                                      highlightbackground=self.backgroundColour,
                                                      highlightthickness=0)

    def clearCanvas(self):
        self.component.delete("all")

    def pixel(self, row: int, col: int, resolutionX: int, resolutionY: int, colour: str):
        if len(colour) != 6:
            return
        scaleX = int(self.getAbsoluteWidth() / max(resolutionX, resolutionY))
        scaleY = int(self.getAbsoluteHeight() / max(resolutionX, resolutionY))
        self.component.create_rectangle(row * scaleX, col * scaleY,
                                        row * scaleX + scaleX, col * scaleY + scaleY,
                                        fill=f"#{colour.strip('#')}")
        self.component.update()

    def drawImage(self, resolutionX: int, resolutionY: int, data: str):
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
        img = Image.open(filePath)
        ratio = (img.size[0] / img.size[1])
        img = img.resize((int(self.getAbsoluteWidth() if ratio > 1 else self.getAbsoluteWidth() * ratio),
                          int(self.getAbsoluteHeight() if ratio < 1 else self.getAbsoluteHeight() / ratio)),
                         Image.NEAREST)
        self.image = ImageTk.PhotoImage(img)
        self.component.create_image(self.getAbsoluteWidth() / 2, self.getAbsoluteHeight() / 2, image=self.image)

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
