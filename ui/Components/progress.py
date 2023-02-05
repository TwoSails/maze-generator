from tkinter import Frame, Canvas

from typing import Dict, Tuple, List

from ui.misc import NoneTypeCheck
from ui.Components import Component


class Progress(Component):
    def __init__(self, parent: Frame, style: Dict, geometry: Tuple[int] | List[int]):
        super().__init__(parent, style, geometry)
        self.setComponent()
        self.colour = NoneTypeCheck(style.get("line-colour"), "cyan")
        self.completeColour = NoneTypeCheck(style.get("backing-colour"), "#555555")
        self.value = NoneTypeCheck(style.get("default"), 50)
        self.fetchData = self.get
        self.initCanvas()
        self.drawLine()

    def setComponent(self):
        self.component: Canvas = Canvas(self.componentFrame, width=self.getAbsoluteWidth(),
                                        height=self.getAbsoluteHeight(),
                                        highlightbackground=self.backgroundColour,
                                        highlightthickness=0,
                                        bg=self.backgroundColour)
        
    def initCanvas(self):
        self.component.delete("all")
        self.component.create_line(self.getAbsoluteHeight() / 2 - 1,
                                   self.getAbsoluteHeight() / 2 - 1,
                                   self.getAbsoluteWidth() - self.getAbsoluteHeight() / 2 - 1,
                                   self.getAbsoluteHeight() / 2 - 1,
                                   width=self.getAbsoluteHeight(),
                                   capstyle="round", fill=self.completeColour)

    def drawLine(self):
        self.component.delete("progress")
        self.component.create_line(self.getAbsoluteHeight() / 2 - 1,
                                   self.getAbsoluteHeight() / 2 - 1,
                                   (self.value / 100) * self.getAbsoluteWidth() - self.getAbsoluteHeight() / 2 - 1,
                                   self.getAbsoluteHeight() / 2 - 1,
                                   width=self.getAbsoluteHeight(),
                                   capstyle="round", fill=self.colour,
                                   tags="progress")

    def increment(self, value):
        self.value += value
        self.value = max([self.value, 0])
        self.value = min([self.value, 100])
        self.drawLine()

    def set(self, value):
        self.value = value
        self.drawLine()

    def get(self):
        return self.value
