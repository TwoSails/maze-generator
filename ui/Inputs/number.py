from tkinter import Frame
from tkinter import ttk

from typing import Optional

from ui.Inputs import Input


class NumberInput(Input):
    def __init__(self, parent: Frame):
        super().__init__(parent)
        self.value = 10
        self.component: Optional[ttk.Spinbox] = None  # To adjust for type hinting
        self.setComponent(ttk.Spinbox(self.componentFrame))

    def setRange(self, _from: int, to: int):
        self.setComponent(ttk.Spinbox(self.componentFrame, _from=_from, to=to))
        self.setValue()
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
