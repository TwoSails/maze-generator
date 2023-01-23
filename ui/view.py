import os
from tkinter import Tk, Frame
import importlib
from typing import Dict

from ui.Config import Config
from ui.Windows import Window


class View(Tk):
    def __init__(self):
        super().__init__()
        self.__config = Config()
        self.wm_title(self.__config.config.get("title"))
        self.geometryDimensions = [min([1440, self.winfo_screenwidth()]), min([1024, self.winfo_screenheight() - 100])]
        self.wm_geometry(f"{self.geometryDimensions[0]}x{self.geometryDimensions[1]}")
        self.wm_resizable(0, 0)
        self.widgets = {}
        self.contentFrame = Frame(self, bg="#ff0000")
        self.contentFrame.pack(fill="both", expand=True)
        self.windows: Dict[str, Window] = {}
        self.makeWindows()

    def loadWidgets(self, widgets=("sidebar", "board")):
        for widget in widgets:
            widget = importlib.import_module(f"ui.Widgets.{widget}")
            if hasattr(widget, "widget"):
                name = getattr(widget, "widget")
                self.widgets[name] = getattr(widget, name)(self.contentFrame, self.geometryDimensions)

    def loadWindow(self, window):
        widgets = window["widgets"]
        for widget in os.listdir("./ui/Widgets/"):
            if os.path.isdir(f"./ui/Widgets/{widget}"):
                continue
            widget = widget.strip(".py")
            widget = importlib.import_module(f"ui.Widgets.{widget}")
            if hasattr(widget, "widget") and getattr(widget, "active"):
                widgetName = getattr(widget, "widget")
                if widgetName not in widgets:
                    continue
                self.widgets[widgetName] = getattr(widget, widgetName)(self.windows[window["name"]],
                                                                       self.__config.config["widgets"].get(widgetName),
                                                                       self.geometryDimensions)
                print(self.widgets)

    def makeWindows(self):
        settings = self.__config.config
        for window in settings["windows"]:
            self.windows[window["name"]] = Window(self.contentFrame,
                                                  window["name"],
                                                  self.__config.config,
                                                  self.geometryDimensions)

    def displayWindow(self, name):
        if name not in self.windows.keys():
            return

        for window in self.windows.keys():
            self.windows[window].destroy()

        self.windows[name].build()
