import pygame

from UIElements.AllUIElements import *
from WindowOverlayHelper.Window import Window

class MatrizenTransponieren(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int):
        super().__init__(screen, x, y, z, width, height)

        self.text = Text(self.screen, 0, 0, 0, 300, 100, "Matrix - Transponieren", fontSize=30)

        self.addObject(self.text)

module = MatrizenTransponieren