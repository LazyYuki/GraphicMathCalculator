import pygame

from UIElements.AllUIElements import *
from WindowOverlayHelper.Window import Window
from UIElements.Matrix import Matrix

class MatrizenTransponieren(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int):
        super().__init__(screen, x, y, z, width, height)

        # w: 1110, h: 800

        # === Main Window

        self.headline = Text(self.screen, 0, 0, 0, self.width, 100, "Matrix - Einfuehrung", fontSize=70, fontPath="Assets/Fonts/HEADLINE.ttf")
        self.headline.center = True
        self.addObject(self.headline)

        self.overall = Window(self.screen, 50, 115, 0, self.width - 100, 270)
        self.transponieren = Window(self.screen, 50, 115 + self.overall.height + 15, 0, self.width - 100, 400)
        self.addObject(self.overall)
        self.addObject(self.transponieren)

        # === Overall
        self.addObject(Text(self.screen, 0, 0, 0, self.overall.width / 4, 50, "Zeilenvektor (m = 1)", fontSize=40, fontPath="Assets/Fonts/Inter.ttf", center=True))
        self.zeilenVektor = Matrix(self.screen, 0, 100, 0, self.overall.width / 4, self.overall.height - 100, 1, 3, fontSize=30)
        self.zeilenVektor.changeSize(1, 3)
        
        self.addObject(self.zeilenVektor)

        

module = MatrizenTransponieren