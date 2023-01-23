from tkinter import Frame
import importlib
import os
from typing import Dict

from ui.Widgets import Widget


class Window:
    def __init__(self, parent: Frame, name, settings, geometry=(0, 0)):
        self.name = name
        self.parentFrame = parent
        self.settings = settings
        self.geometry = geometry
        self.contentFrame = Frame(self.parentFrame)
        self.contentFrame.pack(fill="both", expand=True)
        self.widgets: Dict[str, Widget] = {}

    def loadContent(self):
        widgets = next(w for w in self.settings["windows"] if w["name"] == self.name)["widgets"]
        for widget in os.listdir("./ui/Widgets"):
            if os.path.isdir(f"./ui/Widgets/{widget}"):
                continue

            widget = widget.strip(".py")
            widget = importlib.import_module(f"ui.Widgets.{widget}")
            if hasattr(widget, "widget") and getattr(widget, "active"):
                widgetName = getattr(widget, "widget")
                if widgetName not in widgets:
                    continue
                widgetObj = getattr(widget, widgetName)
                self.widgets[widgetName] = widgetObj(self.contentFrame,
                                                     self.settings["widgets"].get(widgetName),
                                                     self.geometry
                                                     )
                self.widgets[widgetName].display(window=self.name)
                self.widgets[widgetName].buildRows()

    def build(self):
        self.contentFrame.pack(fill="both", expand=True)
        self.loadContent()
        print("Building...")

    def destroy(self):
        self.contentFrame.destroy()
        self.contentFrame = Frame(self.parentFrame)
