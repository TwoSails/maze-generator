from tkinter import Frame

from typing import Dict, Any, Tuple, List

from ui.Components import Row


class Widget:
    def __init__(self, parent: Frame, arrangement: Dict[str, Any], geometry: Tuple[int] | List[int], **kwargs):
        self.parentFrame: Frame = parent
        self.height: float = self.NoneTypeCheck(arrangement.get("height"), 0.0)
        self.width: float = self.NoneTypeCheck(arrangement.get("width"), 0.0)
        self.x: int = self.NoneTypeCheck(arrangement.get("x"))
        self.y: int = self.NoneTypeCheck(arrangement.get("y"))
        self.absoluteCoordinates = self.NoneTypeCheck(arrangement.get("absoluteCoordinates"), False)
        self.absoluteDimensions = self.NoneTypeCheck(arrangement.get("absoluteDimensions"), False)
        self.geometry = geometry
        self.widgetFrame = Frame(self.parentFrame,
                                 height=self.getAbsoluteHeight(),
                                 width=self.getAbsoluteWidth(),
                                 **kwargs)
        self.rows = []

    @staticmethod
    def NoneTypeCheck(arg, null: Any = 0):
        if arg is None:
            return null

        return arg

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
            print(f"x={self.getAbsoluteX()} y={self.getAbsoluteY()} height={self.getAbsoluteHeight()}, width={self.getAbsoluteWidth()}")
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

    def addRow(self):
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
