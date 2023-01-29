from tkinter import Frame
from tkinter import ttk

from typing import Dict, Tuple, List

from ui.Components import Component


class Entry(Component):
    def __init__(self, parent: Frame, style: Dict, geometry: Tuple[int] | List[int]):
        super().__init__(parent, style, geometry)
        self.component: ttk.Entry = ttk.Entry(self.componentFrame)
        self.fetchData = self.get

    def get(self) -> str:
        return self.component.get()
