import pygame

from UIElements.AllUIElements import *
from WindowOverlayHelper.Window import Window

class MatrizenEinführung(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int):
        super().__init__(screen, x, y, z, width, height)

        self.text = Text(self.screen, 0, 0, 0, 300, 100, "Matrix - Einführung", fontSize=30)

        self.addObject(Button(screen, 0, 200, 0, 200, 100, text="Test button"))
        self.addObject(self.text)

module = MatrizenEinführung