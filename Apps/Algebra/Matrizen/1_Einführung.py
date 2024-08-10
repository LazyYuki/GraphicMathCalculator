import pygame

from UIElements.AllUIElements import *
from UIElements.Matrix import Matrix
from WindowOverlayHelper.Window import Window

class MatrizenEinführung(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int):
        super().__init__(screen, x, y, z, width, height)

        self.headline = Text(self.screen, 0, 0, 0, self.width, 100, "Matrix - Einfuehrung", fontSize=70, fontPath="Assets/Fonts/HEADLINE.ttf")
        self.headline.center = True

        self.sliderText = Text(self.screen, 10, 230, 0, 200, 25, "", fontSize=20)
        self.sliderText.center = True
        self.slider = Slider(self.screen, 10, 200, 0, 200, 25, onValueChange=lambda a, b: self.sliderText.setText(str(a.value)))
        
        self.matrix = Matrix(self.screen, 10, 300, 0, 500, 500)
        self.matrix.changeSize(3, 3)

        self.addObject(self.sliderText)
        self.addObject(self.slider)
        self.addObject(self.headline)

        self.addObject(self.matrix)

module = MatrizenEinführung