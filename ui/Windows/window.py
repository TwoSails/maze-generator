from tkinter import Frame
from typing import Dict, Optional, Any

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
        self.injectedStyle = None
        self.injectedWidget = None

    def loadContent(self):
        widgets = []
        for window in self.settings["windows"]:
            if window["name"] == self.name:
                widgets = window["widgets"]

        for widget in widgets:
            shared = self.settings["widgets"].get(widget).get("shared")
            if shared is None:
                shared = []
            elementWindows = self.settings["widgets"].get(widget).get("elements").keys()
            name = self.name
            if self.name in shared:
                name = list(filter(lambda x: x in elementWindows, shared))[0]
            self.widgets[widget] = Widget(self.contentFrame,
                                          self.settings["widgets"].get(widget),
                                          self.geometry,
                                          controller=self.controller)
            self.widgets[widget].display(window=name)
            self.widgets[widget].buildRows()

    def build(self, injectStyle=None, injectWidget=None):
        if injectWidget is not None:
            widgetSettings: Dict[str, Any] = self.settings["widgets"].get(injectWidget)
            elements = widgetSettings.get("elements").get(self.name)
            if elements is not None:
                elements.append(injectStyle)
                self.injectedWidget = injectWidget
                self.injectedStyle = injectStyle
        self.contentFrame.pack(fill="both", expand=True)
        self.loadContent()
        for widget in self.widgets.values():
            widget.place()
        print("Building...")

    def destroy(self):
        if self.injectedStyle is not None and self.injectedWidget is not None:
            elements = self.settings["widgets"].get(self.injectedWidget).get("elements").get(self.name)
            if self.injectedStyle in elements:
                idx = elements.index(self.injectedStyle)
                if idx is not None:
                    elements.pop(idx)
                    print("Removed injected style")
                    # Has to remove injected style as it will remain after destruction in widget settings

        self.contentFrame.destroy()
        self.contentFrame = Frame(self.parentFrame)
