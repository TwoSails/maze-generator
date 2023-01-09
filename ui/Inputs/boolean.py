from tkinter import Frame, IntVar
from tkinter import ttk

from typing import Optional

from ui.Inputs import Input


class BooleanInput(Input):
    def __init__(self, parent: Frame, text: str = ""):
        super().__init__(parent)
        self.state: IntVar = IntVar()
        self.component: Optional[ttk.Checkbutton] = None
        self.setComponent(ttk.Checkbutton(self.componentFrame, text=text, variable=self.state))

    def setState(self, state: Optional[bool]):
        if state is not None:
            self.state.set(int(state))

    def getState(self):
        return bool(self.state.get())
