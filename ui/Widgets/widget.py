from tkinter import Frame

from typing import Dict, Any, Tuple, List
from abc import abstractmethod

from ui.Row import Row
from ui.Inputs import NumberInput, BooleanInput, ButtonInput
from ui.Labels import Text
from ui.misc import NoneTypeCheck


class Widget:
    def __init__(self, parent: Frame, arrangement: Dict[str, Any], geometry: Tuple[int] | List[int], **kwargs):
        self.parentFrame: Frame = parent
        self.style = arrangement
        self.height: float = NoneTypeCheck(arrangement.get("height"), 0.0)
        self.width: float = NoneTypeCheck(arrangement.get("width"), 0.0)
        self.x: int = NoneTypeCheck(arrangement.get("x"))
        self.y: int = NoneTypeCheck(arrangement.get("y"))
        self.absoluteCoordinates = NoneTypeCheck(arrangement.get("absoluteCoordinates"), False)
        self.absoluteDimensions = NoneTypeCheck(arrangement.get("absoluteDimensions"), False)
        self.geometry = geometry
        self.widgetFrame = Frame(self.parentFrame,
                                 height=self.getAbsoluteHeight(),
                                 width=self.getAbsoluteWidth(),
                                 **kwargs)
        self.components = {
            "Text": Text,
            "Row": Row,
            "NumberInput": NumberInput,
            "BooleanInput": BooleanInput,
            "ButtonInput": ButtonInput
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

    def place(self):
        if self.absoluteDimensions:
            self.widgetFrame.place(x=self.getAbsoluteX(),
                                   y=self.getAbsoluteY(),
                                   height=self.getAbsoluteHeight(),
                                   width=self.getAbsoluteWidth())

        else:
            print(f"x={self.getAbsoluteX()} y={self.getAbsoluteY()} height={self.height}, width={self.width}")
            self.widgetFrame.place(x=self.getAbsoluteX(),
                                   y=self.getAbsoluteY(),
                                   relheight=self.height,
                                   relwidth=self.width)

    def addRow(self) -> Row:
        self.rows.append(Row(self.widgetFrame, self.geometry))
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

    @abstractmethod
    def display(self, window: str = ""):
        pass
