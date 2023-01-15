from tkinter import Frame

from typing import Optional


class Row:
    def __init__(self, parent: Frame, geometry):
        self.parentFrame = parent
        self.geometry = geometry
        self.maxWidth = 0
        self.height = 0
        self.expand = False
        self.rowFrame = Frame(parent)
        self.contentLeft = None
        self.contentRight = None

    def destroy(self):
        self.rowFrame.destroy()

    def refresh(self):
        if self.expand:
            self.rowFrame = Frame(self.parentFrame, height=self.height, width=self.maxWidth)
            self.rowFrame.pack()
        else:
            self.rowFrame = Frame(self.parentFrame, height=self.height)
            self.rowFrame.pack()

        if self.contentLeft is not None:
            self.contentLeft.parentFrame = self.rowFrame
            self.contentLeft.refresh()
        if self.contentRight is not None:
            self.contentRight.parentFrame = self.rowFrame
            self.contentRight.refresh()

    def setMaxWidth(self, maxWidth: int, expand: Optional[bool] = None):
        self.maxWidth = maxWidth
        if expand is not None:
            self.expand = expand
            self.refresh()

    def setHeight(self, height):
        self.height = height
        self.refresh()

    def setContentLeft(self, content):
        content.parentFrame = self.rowFrame
        self.contentLeft = content

    def setContentRight(self, content):
        content.parentFrame = self.rowFrame
        self.contentRight = content

    def build(self, index):
        self.rowFrame.grid(row=index, column=0)
        if self.contentLeft is not None:
            self.contentLeft.build()
        if self.contentRight is not None:
            self.contentRight.build()
