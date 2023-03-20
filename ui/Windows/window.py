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
        """
        Loads styling of window and assembles widgets
        """
        widgets = []
        for window in self.settings["windows"]:
            if window["name"] == self.name:
                widgets = window["widgets"]  # Gets names of widgets in window

        for widget in widgets:
            # Determines if a widget is shared across multiple windows
            shared = self.settings["widgets"].get(widget).get("shared")
            if shared is None:
                shared = []
            # gets windows for which the widget assembles for
            elementWindows = self.settings["widgets"].get(widget).get("elements").keys()
            name = self.name
            # determines if widget is shared
            if self.name in shared:
                name = list(filter(lambda x: x in elementWindows, shared))[0]
            # Loads and saves widget
            self.widgets[widget] = Widget(self.contentFrame,
                                          self.settings["widgets"].get(widget),
                                          self.geometry,
                                          controller=self.controller)
            self.widgets[widget].display(window=name)  # Displays current window content
            self.widgets[widget].buildRows()

    def build(self, injectStyle=None, injectWidget=None):
        """
        Displays widget and components on tkinter window
        """
        if injectWidget is not None:  # Programmatic components added to the widget
            # Fetches config settings for widget
            widgetSettings: Dict[str, Any] = self.settings["widgets"].get(injectWidget)
            # Fetches the elements from the config setting
            elements = widgetSettings.get("elements").get(self.name)
            if elements is not None:
                elements.append(injectStyle)  # Adds the programmatic style to the widget elements
                self.injectedWidget = injectWidget  # Logs injected styles
                self.injectedStyle = injectStyle
        self.contentFrame.pack(fill="both", expand=True)
        self.loadContent()
        for widget in self.widgets.values():
            widget.place()
        print("Building...")

    def destroy(self):
        if self.injectedStyle is not None and self.injectedWidget is not None:
            # gets widget elements
            elements = self.settings["widgets"].get(self.injectedWidget).get("elements").get(self.name)
            if self.injectedStyle in elements:
                idx = elements.index(self.injectedStyle)  # Finds where the styling was inserted
                if idx is not None:
                    elements.pop(idx)
                    print("Removed injected style")
                    # Has to remove injected style as it will remain after destruction in widget settings

        self.contentFrame.destroy()
        self.contentFrame = Frame(self.parentFrame)
