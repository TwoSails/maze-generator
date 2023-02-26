from tkinter import Tk, Frame
from typing import Dict

from ui.Config import Config
from ui.Windows import Window
from ui.Controllers import Controller


class View(Tk):
    def __init__(self):
        super().__init__()
        self.__config = Config()
        self.wm_title(self.__config.config.get("title"))
        self.geometryDimensions = [min([1440, self.winfo_screenwidth()]), min([1024, self.winfo_screenheight() - 100])]
        self.wm_geometry(f"{self.geometryDimensions[0]}x{self.geometryDimensions[1]}")
        self.wm_resizable(False, False)
        self.widgets = {}
        self.controller = Controller(self)
        self.contentFrame = Frame(self, bg="#ff0000")
        self.contentFrame.pack(fill="both", expand=True)
        self.windows: Dict[str, Window] = {}
        self.makeWindows()

    def makeWindows(self):
        """
        Creates windows object and passes through settings and controller
        """
        settings = self.__config.config
        for window in settings["windows"]:
            self.windows[window["name"]] = Window(self.contentFrame,
                                                  window["name"],
                                                  self.__config.config,
                                                  self.geometryDimensions,
                                                  controller=self.controller)

    def displayWindow(self, name, injectStyle=None, injectWidget=None):
        """
        Injecting style and widget are used to add elements to a widget during the execution of the program
        This is used to render complex grid information for the Sidebar{cell} widget
        :param name:
        :param injectStyle:
        :param injectWidget:
        :return:
        """
        if name not in self.windows.keys():
            return

        for window in self.windows.keys():
            self.windows[window].destroy()

        self.windows[name].build(injectStyle=injectStyle, injectWidget=injectWidget)
