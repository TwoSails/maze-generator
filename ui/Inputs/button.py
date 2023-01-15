from tkinter import Frame
from tkinter import ttk

from typing import Optional, Dict, Tuple, List

from ui.Components import Component


class ButtonInput(Component):
    def __init__(self, parent: Frame, style: Dict, geometry: Tuple[int] | List[int], text: str, command: Optional[callable] = None):
        super().__init__(parent, style, geometry)
        self.text = text
        self.component = ttk.Button(self.componentFrame, text=self.text, command=command)

    def setCommand(self, command: callable):
        self.component = ttk.Button(self.componentFrame, text=self.text, command=command)
        if self.active:
            self.refresh()
