from tkinter import Frame
from tkinter import ttk
from tkinter import constants as const

from typing import Optional


class Input:
    def __init__(self, parent: Frame):
        self.parentFrame: Frame = parent
        self.componentFrame: Frame = Frame(self.parentFrame)
        self.component: Optional[ttk.Widget] = None

        self.focus = False
        self.active: bool = False

        self.height: int = 26
        self.width: int = 90
        self.padding: int = 0
        self.alignment: const = const.RIGHT

        self.__kwargs = {
            "fill": const.BOTH,
        }

    @staticmethod
    def ValidateMultiTypeInputToInteger(validate):
        if isinstance(validate, str):
            try:
                validate = int(validate)
            except ValueError:
                return None

        validate = abs(validate)
        return validate

    def setComponent(self, component: ttk.Widget):
        if not isinstance(component, ttk.Widget):
            return False
        self.component = component
        return True

    def setBuildStyle(self, **kwargs):
        self.__kwargs.update(**kwargs)

    def setHeight(self, height: int | str):
        height = self.ValidateMultiTypeInputToInteger(height)
        if height is not None:
            self.height = height

    def setWidth(self, width: int | str):
        width = self.ValidateMultiTypeInputToInteger(width)
        if width is not None:
            self.width = width

    def setAlignment(self, alignment: const):
        self.alignment = alignment

    def setPadding(self, padding: int | str):
        padding = self.ValidateMultiTypeInputToInteger(padding)
        if padding is not None:
            self.padding = padding

    def build(self, **kwargs):
        self.__kwargs.update(kwargs)
        self.componentFrame.pack()
        if self.focus:
            self.component.focus_force()
        self.component.pack(padx=self.padding, pady=self.padding,
                            height=self.height,
                            width=self.width,
                            sticky=self.alignment,
                            **self.__kwargs)
        self.active = True

    def destroy(self):
        self.component.destroy()
        self.componentFrame.destroy()
        self.parentFrame.destroy()
        self.active = False

    def refresh(self):
        self.destroy()
        self.build(**self.__kwargs)
