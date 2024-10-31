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

        self.headline = Text(self.screen, 0, 0, 0, self.width, 100, "Vektoren - Einfuehrung", fontSize=70, fontPath="assets/fonts/HEADLINE.ttf")
        self.headline.center = True
        self.addObject(self.headline)

        # self.addObject(Triangle(self.screen, 0, 100, 0, 200, 200, 100, 100, 0, color=(255, 0, 0)))

        # self.ra = rotatableArrow(self.screen, 200, 200, 0, 200, 40, 30, 5, 0, color=(255, 0, 0))
        # self.addObject(self.ra)

        self.coord = Coord3d(self.screen, 50, 120, 0, self.width - 100, 420)
        self.addObject(self.coord)

        

        self.coord.renderMatplotLib()

        self.lol = 0

module = VektorEinführung