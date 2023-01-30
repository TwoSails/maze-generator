from tkinter import Frame
from typing import Dict, Optional

from ui.Widgets import Widget
from ui.Controllers import Controller


class Window:
    def __init__(self, parent: Frame, name, settings, geometry=(0, 0), controller: Optional[Controller] = None):
        self.name = name
        self.parentFrame = parent
        self.settings = settings
        self.geometry = geometry
        self.controller = controller
        self.contentFrame = Frame(self.parentFrame)
        self.contentFrame.pack(fill="both", expand=True)
        self.widgets: Dict[str, Widget] = {}

    def loadContent(self):
        widgets = []
        for window in self.settings["windows"]:
            if window["name"] == self.name:
                widgets = window["widgets"]

        for widget in widgets:
            self.widgets[widget] = Widget(self.contentFrame,
                                          self.settings["widgets"].get(widget),
                                          self.geometry,
                                          controller=self.controller)
            self.widgets[widget].display(window=self.name)
            self.widgets[widget].buildRows()

    def build(self):
        self.contentFrame.pack(fill="both", expand=True)
        self.loadContent()
        for widget in self.widgets.values():
            widget.place()
        print("Building...")

    def destroy(self):
        self.contentFrame.destroy()
        self.contentFrame = Frame(self.parentFrame)
