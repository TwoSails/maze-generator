from tkinter import Frame

from ui.Widgets import Widget

widget = "Board"
active = True


class Board(Widget):
    def __init__(self, parent: Frame, style, geometry):
        super().__init__(parent, style, geometry, bg="#00ff00")
        self.place()

    def display(self, window: str = ""):
        pass

