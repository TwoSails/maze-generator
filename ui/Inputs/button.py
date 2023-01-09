from tkinter import Frame
from tkinter import ttk
from tkinter import constants as const

from typing import Optional

from ui.Inputs import Input


class ButtonInput(Input):
    def __init__(self, parent: Frame, text: str, command: Optional[callable] = None):
        super().__init__(parent)
        self.text = text
        self.setComponent(ttk.Button(self.componentFrame, text=text, command=command))
        self.setHeight(40)
        self.setWidth(119)
        self.setAlignment(const.CENTER)

    def setCommand(self, command: callable):
        self.setComponent(ttk.Button(self.componentFrame, text=self.text, command=command))
        if self.active:
            self.refresh()
