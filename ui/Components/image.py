from tkinter import Frame, Label
from PIL import ImageTk
from PIL import Image as PillowImage

from typing import Dict, Tuple, List

from ui.misc import NoneTypeCheck
from ui.Components import Component


class Image(Component):
    def __init__(self, parent: Frame, style: Dict, geometry: Tuple[int] | List[int]):
        super().__init__(parent, style, geometry)
        self.filePath = NoneTypeCheck(style.get("filename"), None)
        self.text = NoneTypeCheck(style.get("text"), None)
        self.textColour = NoneTypeCheck(style.get("colour"), "#ffffff")
        self.justify = NoneTypeCheck(style.get("justify"), "w")
        self.transformation = NoneTypeCheck(style.get("transformation"), None)
        self.anchoring = lambda x: "w" if x == "left" else "e" if x == "right" else "center"
        self.textLabel = None
        self.img = None
        if self.filePath is not None:
            self.loadImage()
            self.setComponent()
        self.command = NoneTypeCheck(style.get("command"), None)
        if self.command is not None:
            self.component.bind("<Button-1>", self.command)

    def setTextLabel(self):
        self.textLabel = Label(self.componentFrame,
                               text=self.text,
                               font=(NoneTypeCheck(self.style.get("font"), ""),
                                     NoneTypeCheck(self.style.get("font-size"), 18),
                                     NoneTypeCheck(self.style.get("font-weight"), "")),
                               fg=self.textColour,
                               bg=self.backgroundColour,
                               anchor=self.anchoring(self.justify)
                               )

    def loadImage(self):
        img = PillowImage.open(self.filePath)
        img = img.resize((int(self.getAbsoluteWidth()), int(self.getAbsoluteHeight())), PillowImage.NEAREST)
        if self.transformation is not None:
            match self.transformation:
                case "Rotation.one":
                    img = img.transpose(PillowImage.Transpose.ROTATE_90)
                case "Rotation.two":
                    img = img.transpose(PillowImage.Transpose.ROTATE_180)
                case "Rotation.three":
                    img = img.transpose(PillowImage.Transpose.ROTATE_270)
                case "Axis.X":
                    img = img.transpose(PillowImage.Transpose.FLIP_TOP_BOTTOM)
                case "Axis.Y":
                    img = img.transpose(PillowImage.Transpose.FLIP_LEFT_RIGHT)
                case _:
                    img = img
        self.img = ImageTk.PhotoImage(img)

    def setComponent(self):
        self.component = Label(self.componentFrame, image=self.img,
                               bg=self.backgroundColour,
                               highlightbackground=self.backgroundColour,
                               highlightthickness=0)
        self.component.image = self.img
        if self.text is not None:
            self.setTextLabel()

    def update(self, text="", filename=""):
        self.text = text,
        self.filePath = filename

        if self.text != "":
            if self.text is not None and self.textLabel is None:
                self.setTextLabel()
            self.textLabel.config(text=text)
        if filename == "":
            self.img = ""
        else:
            self.loadImage()
        self.component.config(image=self.img)

    def border(self, border=None):
        if border is None:
            self.componentFrame.config(bg=self.backgroundColour, padx=0, pady=0)
            return
        self.componentFrame.config(bg=border, padx=3, pady=3)
