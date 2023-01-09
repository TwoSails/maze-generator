from tkinter import Frame

from ui.Widgets import Widget

widget = "Sidebar"  # This is required to load the widget class as this is a known variable name


class Sidebar(Widget):
    def __init__(self, parent: Frame, geometry):
        super().__init__(parent, {
            "height": 1.0,
            "width": 0.25,
            "x": 0,
            "y": 0,
            "absoluteCoordinates": True,
            "absoluteDimensions": False
        }, geometry, bg="#ffffff")
        self.place()

    def view(self):
        pass

    def build(self):
        self.place()
        self.buildRows()
