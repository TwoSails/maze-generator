from tkinter import Frame

from ui.Widgets import Widget
from ui.Row import Row
from ui.misc import NoneTypeCheck


widget = "Sidebar"  # This is required to load the widget class as this is a known variable name
active = True


class Sidebar(Widget):
    def __init__(self, parent: Frame, style, geometry):
        super().__init__(parent, style, geometry)
        self.place()

    def __explore(self, style):
        elementType = style.get("type")
        if elementType is None:
            return
        if elementType == "Row":
            row = Row(self.getRow(-1),
                      self.geometry,
                      x=NoneTypeCheck(style.get("x"), 0),
                      y=NoneTypeCheck(style.get("y"), 0),
                      bg=NoneTypeCheck(style.get("background-colour"), "#ffffff"))
            row.setContentLeft(self.__explore(style["contentLeft"]))
            row.setContentRight(self.__explore(style["contentRight"]))
            return row

        element = self.components[style["type"]]
        if elementType == "Text":
            textComponent = element(self.getRow(-1).rowFrame, style, self.geometry)
            return textComponent

        if elementType == "BooleanInput":
            return element(self.getRow(-1).rowFrame, style, self.geometry, text=style.get("text"))

        inputComponent = element(self.getRow(-1).rowFrame, style, self.geometry)
        return inputComponent

    def display(self, window: str = ""):
        elements = self.style["elements"][window]
        for element in elements:
            elementType = element["type"]
            if elementType not in self.components.keys():
                continue
            if elementType == "Row":
                row = self.addRow(x=NoneTypeCheck(element.get("x"), 0),
                                  y=NoneTypeCheck(element.get("y"), 0),
                                  bg=NoneTypeCheck(element.get("background-colour"), "#ffffff"))
                if element["contentLeft"] is not None:
                    row.setContentLeft(self.__explore(element["contentLeft"]))
                if element["contentRight"] is not None:
                    row.setContentRight(self.__explore(element["contentRight"]))

    def build(self):
        self.place()
        self.buildRows()
