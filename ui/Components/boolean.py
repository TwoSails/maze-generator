from tkinter import Frame, IntVar
from tkinter import ttk

from typing import Optional, Dict, Tuple, List

from ui.misc import NoneTypeCheck
from ui.Components import Component


class BooleanInput(Component):
    """
    Represents checkbox input
    """
    def __init__(self, parent: Frame, style: Dict, geometry: Tuple[int] | List[int]):
        super().__init__(parent, style, geometry)
        self.state: IntVar = IntVar()
        self.component: Optional[ttk.Checkbutton] = None
        self.text = NoneTypeCheck(style.get("text"), "Boolean")
        self.fetchData = self.get
        self.setComponent()

    def setComponent(self):
        self.component = ttk.Checkbutton(self.componentFrame, text=self.text,
                                         variable=self.state)

    def setState(self, state: Optional[bool]):
        """
        Sets whether checkbox is selected
        """
        if state is not None:
            self.state.set(int(state))

    def get(self):
        return bool(self.state.get())
