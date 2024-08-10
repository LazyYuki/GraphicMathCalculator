import pygame

from UIElements.AllUIElements import *
from UIElements.Matrix import Matrix
from WindowOverlayHelper.Window import Window

class MatrizenEinführung(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int):
        super().__init__(screen, x, y, z, width, height)

        self.headline = Text(self.screen, 0, 0, 0, self.width, 100, "Matrix - Einfuehrung", fontSize=70, fontPath="Assets/Fonts/HEADLINE.ttf")
        self.headline.center = True

        self.matrix = Matrix(self.screen, 340, 200, 0, 600, 600)
        self.matrix.changeSize(3, 3)

        t = Text(self.screen, 10, 200, 0, 100, 25, "m:", fontSize=20)
        t.verticalCenter = True
        self.addObject(t)
        t = Text(self.screen, 10, 230, 0, 100, 25, "n:", fontSize=20)
        t.verticalCenter = True
        self.addObject(t)

        s = Slider(self.screen, 120, 200, 0, 200, 25, onValueChange=lambda a, b: self.matrix.changeSize(m = int(a.value)))
        s.maxValue = 5
        self.addObject(s)

        f = Slider(self.screen, 120, 230, 0, 200, 25, onValueChange=lambda a, b: self.matrix.changeSize(n = int(a.value)))
        f.maxValue = 5
        self.addObject(f)

        self.addObject(self.headline)

        self.addObject(self.matrix)

module = MatrizenEinführung