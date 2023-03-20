from tkinter import Frame, INSERT
from tkinter.scrolledtext import ScrolledText

from typing import Dict, Tuple, List

from ui.misc import NoneTypeCheck
from ui.Components import Component


class Paragraph(Component):
    """
    Tkinter long text component
    """
    def __init__(self, parent: Frame, style: Dict, geometry: Tuple[int] | List[int]):
        super().__init__(parent, style, geometry)
        self.setComponent()

    def setComponent(self):
        self.component = ScrolledText(self.componentFrame,
                                      font=(NoneTypeCheck(self.style.get("font"), ""),
                                            NoneTypeCheck(self.style.get("font-weight"), ""),
                                            NoneTypeCheck(self.style.get("font-size"), 20)),
                                      width=self.getAbsoluteWidth(),
                                      height=self.getAbsoluteHeight())

    def insert(self, line):
        self.component.insert(
            INSERT,
            f"{line}\n")
