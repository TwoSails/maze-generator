from tkinter import Tk, Frame
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
