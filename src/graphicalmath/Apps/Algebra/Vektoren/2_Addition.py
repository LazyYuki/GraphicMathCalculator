import pygame

from UIElements.AllUIElements import *
from UIElements.Coord3d import *
from WindowOverlayHelper.Window import Window
from UIElements.geometricWriting import *

class VektorEinführung(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int):
        super().__init__(screen, x, y, z, width, height)

        # w: 1110, h: 800

        # === Main Window

        self.headline = Text(self.screen, 0, 0, 0, self.width, 100, "Vektoren - Addition", fontSize=70, fontPath="assets/fonts/HEADLINE.ttf")
        self.headline.center = True
        self.addObject(self.headline)

module = VektorEinführung