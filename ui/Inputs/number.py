from tkinter import Frame
from tkinter import ttk

from typing import Optional, Tuple, List, Dict

from ui.Components import Component


class NumberInput(Component):
    def __init__(self, parent: Frame, style: Dict, geometry: Tuple[int] | List[int], from_: int = 0, to: int = 100):
        super().__init__(parent, style, geometry)
        self.fromVal = from_
        self.toVal = to
        self.value = 10
        self.component = ttk.Spinbox(self.componentFrame, from_=self.fromVal, to=self.toVal)

    def setRange(self, _from: int, to: int):
        self.fromVal = _from
        self.toVal = to
        self.component = ttk.Spinbox(self.componentFrame, from_=self.fromVal, to=self.toVal)
        if self.active:
            self.refresh()

    def setValue(self, value: Optional[int] = None):
        if value is None:
            value = self.value
        else:
            self.value = value

        self.component.set(value)

    def getInput(self):
        return self.component.get()
