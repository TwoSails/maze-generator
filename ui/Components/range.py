from tkinter import Frame, DoubleVar
from tkinter.ttk import Scale

from typing import Dict, Tuple, List

from ui.misc import NoneTypeCheck
from ui.Components import Component


class Range(Component):
    def __init__(self, parent: Frame, style: Dict, geometry: Tuple[int] | List[int]):
        super().__init__(parent, style, geometry)
        self.start = NoneTypeCheck(style.get("start"), 0)
        self.end = NoneTypeCheck(style.get("end"), 10)
        self.defaultValue = NoneTypeCheck(style.get("default"), 1)
        self.value = DoubleVar()
        self.fetchData = self.get
        self.setComponent()

    def setComponent(self):
        self.component = Scale(self.componentFrame,
                               from_=self.start,
                               to=self.end,
                               variable=self.value,
                               value=self.defaultValue)

    def get(self):
        return self.value.get()
