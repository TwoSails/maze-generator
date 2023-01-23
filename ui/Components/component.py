from tkinter import Frame

from typing import Dict, Tuple, List, Optional

from ui.misc import NoneTypeCheck


class Component:
    def __init__(self, parent: Frame, style: Dict, geometry: Tuple[int] | List[int]):
        self.parentFrame: Frame = parent
        self.style = style
        self.geometry = geometry
        self.height: float = NoneTypeCheck(style.get("height"), 0.0)
        self.width: float = NoneTypeCheck(style.get("width"), 0.0)
        self.x: int = NoneTypeCheck(style.get("x"))
        self.y: int = NoneTypeCheck(style.get("y"))
        self.backgroundColour: str = NoneTypeCheck(style.get("background-colour"), "")
        self.internalPaddingX: int = NoneTypeCheck(style.get("i-padding-x"), 0)
        self.internalPaddingY: int = NoneTypeCheck(style.get("i-padding-y"), 0)
        self.componentFrame: Frame = Frame(self.parentFrame,
                                           height=self.getAbsoluteHeight(),
                                           width=self.getAbsoluteWidth(),
                                           bg=self.backgroundColour)
        self.component = None
        self.active = False
        self.build()

    def getAbsoluteWidth(self):
        width: str | float = self.width
        if "r" in str(width):
            width = float(width.strip("r"))
            return width * self.geometry[0]
        return width

    def getAbsoluteHeight(self):
        height: str | float = self.height
        if "r" in str(height):
            height = float(height.strip("r"))
            return height * self.geometry[1]
        return height

    def getAbsoluteX(self):
        x: str | float = self.x
        if "r" in str(x):
            x = float(x.strip("r"))
            return x * self.geometry[0]
        return x

    def getAbsoluteY(self):
        y: str | float = self.y
        if "r" in str(y):
            y = float(y.strip("r"))
            return y * self.geometry[1]
        return y

    def getRelativeX(self):
        return self.getAbsoluteX() / self.geometry[0]

    def getRelativeY(self):
        return self.getAbsoluteY() / self.geometry[1]

    def build(self, alignment: Optional[int] = None):
        print(f"Building {self.style.get('type')} Component: {self.active}")
        if self.component is None:
            return False
        if alignment is None:
            self.componentFrame.pack(anchor="w",
                                     ipadx=self.internalPaddingX,
                                     ipady=self.internalPaddingY)
        else:
            self.componentFrame.grid(row=0, column=alignment,
                                     ipadx=self.internalPaddingX,
                                     ipady=self.internalPaddingY)
        self.component.place(relx=self.getRelativeX(),
                             rely=self.getRelativeY(),
                             height=self.getAbsoluteHeight(),
                             width=self.getAbsoluteWidth())
        self.active = True
        return True

    def destroy(self):
        if self.component is None or not self.active:
            return False
        self.component.destroy()
        self.componentFrame.destroy()
        print(f"Destroyed {self.style.get('type')} Component")

    def refresh(self):
        if self.active:
            self.destroy()
        self.build()
