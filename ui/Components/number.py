from tkinter import Frame, INSERT
from tkinter import ttk

from typing import Optional, Tuple, List, Dict

from ui.misc import NoneTypeCheck
from ui.Components import Component


class NumberInput(Component):
    def __init__(self, parent: Frame, style: Dict, geometry: Tuple[int] | List[int]):
        super().__init__(parent, style, geometry)
        self.fromVal = NoneTypeCheck(style.get("from"), 0)
        self.toVal = NoneTypeCheck(style.get("to"), 50)
        self.value = NoneTypeCheck(style.get("default"), 5)
        self.fetchData = self.get
        self.setComponent()

    def setComponent(self):
        self.component = ttk.Spinbox(self.componentFrame, from_=self.fromVal, to=self.toVal)
        self.component.insert(INSERT, self.value)

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

    def insert(self, value):
        self.component.delete(0, 'end')
        self.component.insert(INSERT, value)

    def get(self):
        try:
            data = self.component.get()
            if isinstance(data, str):
                data = 0 if data == "" else int(data)

            data = max(int(self.fromVal), data)
            data = min(int(self.toVal), data)
            self.insert(data)
            return data
        except ValueError:
            return 0
