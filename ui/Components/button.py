from tkinter import Frame, Canvas
from tkinter import ttk

from typing import Optional, Dict, Tuple, List

from ui.misc import NoneTypeCheck
from ui.Components import Component


class ButtonInput(Component):
    """
    Native button widget
    """
    def __init__(self, parent: Frame,
                 style: Dict,
                 geometry: Tuple[int] | List[int],
                 command: Optional[callable] = None):
        super().__init__(parent, style, geometry)
        self.text = NoneTypeCheck(style.get("text"), "Button")
        self.command = command
        self.setComponent()

    def setComponent(self):
        self.component = ttk.Button(self.componentFrame, text=self.text, command=self.command)

    def setCommand(self, command: callable):
        """
        Sets tkinter action on button interaction
        """
        self.component = ttk.Button(self.componentFrame, text=self.text, command=command)
        if self.active:
            self.refresh()


class Button(Component):
    """
    Custom button object built from a canvas for more styling options
    """
    def __init__(self, parent: Frame,
                 style: Dict,
                 geometry: Tuple[int] | List[int],
                 command: Optional[callable] = None):
        super().__init__(parent, style, geometry)
        self.command = command
        self.text = NoneTypeCheck(style.get("text"), "Button")
        self.font = (NoneTypeCheck(style.get("font"), ""),
                     NoneTypeCheck(style.get("font-size"), 20),
                     NoneTypeCheck(style.get("font-weight"), ""))
        self.setComponent()

    def setComponent(self):
        # Draws button in a canvas
        self.component: Canvas = Canvas(self.componentFrame, width=self.getAbsoluteWidth(),
                                        height=self.getAbsoluteHeight(),
                                        highlightbackground=self.backgroundColour,
                                        highlightthickness=0,
                                        bg=NoneTypeCheck(self.style.get("button-colour"), "#ffffff"))

        if self.command is not None:
            self.component.bind("<Button-1>", self.command)  # Adds command through binding
        self.component.create_text(self.getAbsoluteWidth() - (int(self.font[1]) * len(self.text) / 1.5),
                                   (self.getAbsoluteHeight() - int(self.font[1])),
                                   text=self.text,
                                   font=self.font,
                                   fill=NoneTypeCheck(self.style.get("colour"), "#000000"))

    def setCommand(self, command: callable):
        self.component.bind("<Button-1>", command)
