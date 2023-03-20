from tkinter import Frame, Label

from typing import Dict, Tuple, List

from ui.misc import NoneTypeCheck
from ui.Components import Component


class Text(Component):
    """
    Tkinter label component
    """
    def __init__(self, parent: Frame, style: Dict, geometry: Tuple[int] | List[int]):
        super().__init__(parent, style, geometry)
        self.text = NoneTypeCheck(style.get("text"), "")
        self.textColour = NoneTypeCheck(style.get("colour"), "#ffffff")
        self.justify = NoneTypeCheck(style.get("justify"), "w")
        self.anchoring = lambda x: "w" if x == "left" else "e" if x == "right" else "center"
        self.setComponent()

    def setComponent(self):
        self.component = Label(self.componentFrame,
                               text=self.text,
                               font=(NoneTypeCheck(self.style.get("font"), ""),
                                     NoneTypeCheck(self.style.get("font-size"), 20),
                                     NoneTypeCheck(self.style.get("font-weight"), "")),
                               fg=self.textColour,
                               bg=self.backgroundColour,
                               anchor=self.anchoring(self.justify)
                               )

    def update(self, text):
        self.component.config(text=text)
        self.text = text
