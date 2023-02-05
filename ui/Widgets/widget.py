from tkinter import Frame

from typing import Dict, Any, Tuple, List, Optional

from ui.Layout import Row, Grid
from ui.Components import NumberInput, BooleanInput, ButtonInput, Button, Text, Entry, Image, Canvas, Range, \
    Paragraph, Progress
from ui.misc import NoneTypeCheck

from ui.Controllers import Controller


class Widget:
    def __init__(self, parent: Frame, arrangement: Dict[str, Any], geometry: Tuple[int] | List[int],
                 controller: Optional[Controller] = None,
                 **kwargs):
        self.parentFrame: Frame = parent
        self.style = arrangement
        self.height: float = NoneTypeCheck(arrangement.get("height"), 0.0)
        self.width: float = NoneTypeCheck(arrangement.get("width"), 0.0)
        self.x: int = NoneTypeCheck(arrangement.get("x"))
        self.y: int = NoneTypeCheck(arrangement.get("y"))
        self.absoluteCoordinates = NoneTypeCheck(arrangement.get("absoluteCoordinates"), False)
        self.absoluteDimensions = NoneTypeCheck(arrangement.get("absoluteDimensions"), False)
        self.backgroundColour = NoneTypeCheck(arrangement.get("background-colour"), "#ffffff")
        self.geometry = geometry
        self.widgetFrame = Frame(self.parentFrame,
                                 height=self.getAbsoluteHeight(),
                                 width=self.getAbsoluteWidth(),
                                 bg=self.backgroundColour,
                                 **kwargs)
        self.controller = controller
        self.components = {
            "Grid": Grid,
            "Row": Row,
            "Text": Text,
            "NumberInput": NumberInput,
            "BooleanInput": BooleanInput,
            "ButtonInput": ButtonInput,
            "Button": Button,  # Canvas widget so custom style/shape
            "Entry": Entry,
            "Image": Image,
            "Canvas": Canvas,
            "Range": Range,
            "Paragraph": Paragraph,
            "Progress": Progress
        }
        self.rows = []

    def getAbsoluteWidth(self):
        return self.width if self.absoluteDimensions else self.width * self.geometry[0]

    def getAbsoluteHeight(self):
        return self.height if self.absoluteDimensions else self.height * self.geometry[1]

    def getAbsoluteX(self):
        return self.x if self.absoluteCoordinates else self.x * self.geometry[0]

    def getAbsoluteY(self):
        return self.y if self.absoluteCoordinates else self.y * self.geometry[1]

    def getRelativeX(self):
        return self.getAbsoluteX() / self.geometry[0]

    def getRelativeY(self):
        return self.getAbsoluteY() / self.geometry[1]

    def place(self):
        if self.absoluteDimensions:
            self.widgetFrame.place(x=self.getAbsoluteX(),
                                   y=self.getAbsoluteY(),
                                   height=self.getAbsoluteHeight(),
                                   width=self.getAbsoluteWidth())

        else:
            self.widgetFrame.place(relx=self.getRelativeX(),
                                   rely=self.getRelativeY(),
                                   relheight=self.height,
                                   relwidth=self.width)

    def addRow(self, x: int = 0, y: int = 0, bg: Optional[str] = "", **kwargs) -> Row:
        self.rows.append(Row(self.widgetFrame, self.geometry, x=x, y=y, bg=bg, **kwargs))
        return self.rows[-1]

    def buildRows(self):
        for index, row in enumerate(self.rows):
            row.build(index)

    def getRow(self, idx):
        if idx < len(self.rows):
            return self.rows[idx]

    def refreshRows(self):
        for row in self.rows:
            row.refresh()

    def insertRow(self, idx: int, row: Row):
        if idx + 1 >= len(self.rows):
            return

        self.rows.insert(idx + 1, row)

    def configureRow(self, row, style):
        if "width" in style:
            row.setMaxWidth(style.get("width"))
        if style["contentLeft"] is not None:
            row.setContentLeft(self.explore(style["contentLeft"]))
        if style["contentRight"] is not None:
            row.setContentRight(self.explore(style["contentRight"]))
        return row

    def explore(self, style):
        if style is None:
            return
        elementType = style.get("type")
        if elementType is None:
            return
        if elementType == "Row":
            row = Row(self.getRow(-1).rowFrame,
                      self.geometry,
                      x=NoneTypeCheck(style.get("x")),
                      y=NoneTypeCheck(style.get("y")),
                      bg=NoneTypeCheck(style.get("background-colour"), None),
                      tag=NoneTypeCheck(style.get("tag"), ""))
            row = self.configureRow(row, style)
            self.controller.addComponent(row.tag, row)
            return row

        if elementType == "Grid":
            grid = Grid(self.getRow(-1).rowFrame, style, self.geometry)
            for elementStyle in style["elements"]:
                element = self.explore(elementStyle)
                grid.addElement(element)
                self.controller.addComponent(element.tag, element)
            self.controller.addComponent(grid.tag, grid)
            return grid

        element = self.components[elementType]
        command = style.get("command")
        if elementType in ["Button", "ButtonInput"] and command is not None:
            command = getattr(self.controller, command)
            component = element(self.getRow(-1).rowFrame, style, self.geometry, command=command)
        else:
            component = element(self.getRow(-1).rowFrame, style, self.geometry)
        self.controller.addComponent(component.tag, component)
        return component

    def display(self, window: str = ""):
        elements = self.style["elements"][window]
        for element in elements:
            elementType = element["type"]
            if elementType not in self.components.keys():
                continue
            if elementType == "Row":
                row = self.addRow(x=NoneTypeCheck(element.get("x"), 0),
                                  y=NoneTypeCheck(element.get("y"), 0),
                                  bg=NoneTypeCheck(element.get("background-colour"), "#ffffff"),
                                  tag=NoneTypeCheck(element.get("tag"), ""))
                self.configureRow(row, element)
                self.controller.addComponent(row.tag, row)

    def build(self):
        self.place()
        self.buildRows()
