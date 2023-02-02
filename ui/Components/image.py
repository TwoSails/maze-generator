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
        self.anchoring = lambda x: "w" if x == "left" else "e" if x == "right" else "center"
        if self.filePath is not None:
            img = PillowImage.open(self.filePath)
            img = img.resize((int(self.getAbsoluteWidth()), int(self.getAbsoluteHeight())), PillowImage.NEAREST)
            img = ImageTk.PhotoImage(img)
            self.component = Label(self.componentFrame, image=img,
                                   bg=self.backgroundColour,
                                   highlightbackground=self.backgroundColour,
                                   highlightthickness=0)
            self.component.image = img
            if self.text is not None:
                self.textLabel = Label(self.componentFrame,
                                       text=self.text,
                                       font=(NoneTypeCheck(style.get("font"), ""),
                                             NoneTypeCheck(style.get("font-size"), 20),
                                             NoneTypeCheck(style.get("font-weight"), "")),
                                       fg=self.textColour,
                                       bg=self.backgroundColour,
                                       anchor=self.anchoring(self.justify)
                                       )
