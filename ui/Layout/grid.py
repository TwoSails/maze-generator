from tkinter import Frame

from typing import List

from ui.misc import NoneTypeCheck
from ui.Components import Component


class Grid:
    def __init__(self, parent: Frame, style, geometry):
        self.style = style
        self.parentFrame = parent
        self.geometry = geometry
        self.width = NoneTypeCheck(style.get("width"), 100)
        self.height = NoneTypeCheck(style.get("height"), 100)
        self.x = NoneTypeCheck(style.get("x"), 0)
        self.y = NoneTypeCheck(style.get("y"), 0)
        self.columns = NoneTypeCheck(style.get("columns"), "flex")
        self.padding = NoneTypeCheck(style.get("column-padding"), 10)
        self.backgroundColour = NoneTypeCheck(style.get("background-colour"), "#ffffff")
        self.tag = NoneTypeCheck(style.get("tag"), "")

        self.gridFrame = Frame(parent,
                               width=self.getAbsoluteWidth(),
                               height=self.getAbsoluteHeight(),
                               bg=self.backgroundColour)
        self.elements: List[Component] = []
        self.grid: List[Frame] = []

    def getAbsoluteWidth(self):
        width: str | float = self.width
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

    def addElement(self, element: Component):
        """
        Adds component to the grid
        """
        self.grid.append(Frame(self.gridFrame, bg=self.backgroundColour))
        element.parentFrame = self.grid[-1]
        self.elements.append(element)

    def addStrictElement(self, element: Component):
        """
        Used to add component whilst grid is active
        """
        self.grid.append(Frame(self.gridFrame, bg=self.backgroundColour))
        element.setParentFrame(self.grid[-1])
        self.elements.append(element)

    def reassembleElements(self):
        """
        Force refresh of all elements to assign new parent frames
        """
        self.grid = []
        for element in self.elements:
            self.grid.append(Frame(self.gridFrame, bg=self.backgroundColour))
            element.parentFrame = self.grid[-1]

    def build(self, *_, drop: bool = False, coords=None):
        """
        Displays the grid and elements on tkinter window
        "_" parameter Catches any positional arguments which are required, caused by additional parameters in config
        """
        if coords is None:
            coords = []
        width = [element.getAbsoluteWidth() + self.padding for element in self.elements]
        rowWidth = 0
        rows: List[List[Component]] = [[]]
        # Determine position of element in grid
        for idx, elementWidth in enumerate(width):
            rowWidth += elementWidth
            if (rowWidth >= self.getAbsoluteWidth() or
               len(rows[-1]) >= (1000 if self.columns == "flex" else self.columns)):  # How many elements per row
                rows.append([self.elements[idx]])
                rowWidth = 0
            else:
                rows[-1].append(self.elements[idx])

        index = 0

        for idx, row in enumerate(rows):
            for col, element in enumerate(row):
                element.build(drop=True, coords=[idx + 1, col + 1])  # Building elements passing through grid location
                self.grid[index].pack()
                index += 1
        if drop and len(coords) == 2:
            self.gridFrame.grid(row=coords[0], column=coords[1])
        else:
            self.gridFrame.place(relx=self.getRelativeX(), rely=self.getRelativeY())

    def refresh(self):
        """
        Force reloads components onto tkinter window
        """
        self.gridFrame.destroy()
        self.gridFrame = Frame(self.parentFrame,
                               width=self.getAbsoluteWidth(),
                               height=self.getAbsoluteHeight(),
                               bg=self.backgroundColour)
        for frame in self.grid:
            frame.destroy()
        self.reassembleElements()
        self.build()

    def destroy(self):
        """
        Removes the component and elements from tkinter window
        """
        self.gridFrame.destroy()
        for element in self.elements:
            if hasattr(element, "destroy"):
                element.destroy()
