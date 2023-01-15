from tkinter import Frame

from ui.Widgets import Widget
from ui.Row import Row

widget = "Sidebar"  # This is required to load the widget class as this is a known variable name
active = True


class Sidebar(Widget):
    def __init__(self, parent: Frame, style, geometry):
        super().__init__(parent, style, geometry, bg="#000000")
        self.place()

    def __explore(self, style):
        elementType = style["type"]
        if elementType == "Row":
            row = Row(self.getRow(-1), self.geometry)
            row.setContentLeft(self.__explore(style["contentLeft"]))
            row.setContentRight(self.__explore(style["contentRight"]))
            return row

        element = self.components[style["type"]]
        if elementType == "Text":
            textComponent = element(self.getRow(-1).rowFrame, style, self.geometry)
            return textComponent

        inputComponent = element(self.getRow(-1).rowFrame, style, self.geometry)
        return inputComponent

    def display(self, window: str = ""):
        elements = self.style["elements"][window]
        for element in elements:
            elementType = element["type"]
            if elementType not in self.components.keys():
                continue
            if elementType == "Row":
                row = self.addRow()
                row.setContentLeft(self.__explore(element["contentLeft"]))

    def build(self):
        self.place()
        self.buildRows()
