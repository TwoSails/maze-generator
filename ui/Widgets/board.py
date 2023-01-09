from tkinter import Frame

from ui.Widgets import Widget

widget = "Board"


class Board(Widget):
    def __init__(self, parent: Frame, geometry):
        super().__init__(parent, {
            "height": 1.0,
            "width": 0.75,
            "x": 0.25,
            "y": 0,
            "absoluteCoordinates": False,
            "absoluteDimensions": False

        }, geometry, bg="#00ff00")
        self.place()

