from tkinter import Frame, Label

from typing import Dict, Tuple, List

from ui.misc import NoneTypeCheck
from ui.Components import Component


class Text(Component):
    def __init__(self, parent: Frame, style: Dict, geometry: Tuple[int] | List[int]):
        super().__init__(parent, style, geometry)
        self.text = NoneTypeCheck(style.get("text"), "")
        self.component = Label(self.componentFrame,
                               text=self.text,
                               font=(NoneTypeCheck(style.get("font"), ""),
                                     NoneTypeCheck(style.get("font-size"), 20),
                                     NoneTypeCheck(style.get("font-weight"), ""))
                               )
