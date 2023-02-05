from tkinter import Frame

from typing import Optional


class Row:
    def __init__(self, parent: Frame, geometry, x=0, y=0, bg: Optional[str] = None, tag: str = ""):
        self.parentFrame = parent
        self.geometry = geometry
        self.maxWidth = 0
        self.height = 0
        self.x = x
        self.y = y
        self.expand = False
        self.rowFrame = Frame(parent, bg=bg)
        self.contentLeft = None
        self.contentRight = None
        self.tag = tag

    def getAbsoluteWidth(self):
        width: str | float = self.maxWidth
        if "r" in str(width):
            width = float(width.strip("r"))
            return width * self.geometry[0]
        return width

    def getAbsoluteHeight(self):
        height: str | float = self.height
        if "r" in str(height):
            height = float(height.strip("r"))
            return height * self.geometry[1]
        return height

    def getAbsoluteX(self):
        x: str | float = self.x
        if "r" in str(x):
            x = float(x.strip("r"))
            return x * self.geometry[0]
        return x

    def getAbsoluteY(self):
        y: str | float = self.y
        if "r" in str(y):
            y = float(y.strip("r"))
            return y * self.geometry[1]
        return y

    def getRelativeX(self):
        return self.getAbsoluteX() / self.geometry[0]

    def getRelativeY(self):
        return self.getAbsoluteY() / self.geometry[1]

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
        if content is None:
            return
        content.parentFrame = self.rowFrame
        self.contentLeft = content

    def setContentRight(self, content):
        if content is None:
            return 
        content.parentFrame = self.rowFrame
        self.contentRight = content

    def build(self, *_, drop: bool = False, coords=None):
        if coords is None:
            coords = []
        if drop and len(coords) == 2:
            self.rowFrame.grid(row=coords[0], column=coords[1])
        else:
            self.rowFrame.place(relx=self.getRelativeX(), rely=self.getRelativeY())
        if self.contentLeft is not None:
            self.contentLeft.build(0)
        if self.contentRight is not None:
            self.contentRight.build(1)

    def remove(self, left=False, right=False):
        if left and self.contentLeft is not None:
            if hasattr(self.contentLeft, "destroy"):
                self.contentLeft.destroy()
            self.contentLeft = None
        if right and self.contentRight is not None:
            if hasattr(self.contentRight, "destroy"):
                self.contentRight.destroy()
            self.contentRight = None
