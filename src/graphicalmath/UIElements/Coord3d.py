import pygame

from WindowOverlayHelper.WindowObject import WindowObject
from EventManager.EventArgs import MouseEventArgs, KeyboardEventArgs

class Rect(WindowObject):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int) -> None:
        super().__init__(screen, x, y, z, width, height)


    def changeBorderRadius(self, br: int):
        self.br_tr = br
        self.br_br = br
        self.br_tl = br
        self.br_bl = br
