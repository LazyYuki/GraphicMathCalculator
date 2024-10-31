import pygame

from WindowOverlayHelper.Window import Window
from EventManager.EventArgs import MouseEventArgs, KeyboardEventArgs
from UIElements.AllUIElements import *
from UIElements.Matrix import *

from math_calc.Vector import Vector3d

class Vector(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int) -> None:
        super().__init__(screen, x, y, z, width, height)

        self.m = Matrix(self.screen, 0, 0, 0, self.width, self.height)
        self.m.setCenter(True)
        self.m.changeSize(3, 1)

        self.addObject(self.m)

    def getVector(self):
        return Vector3d(self.m.numberMatrix[0][0], self.m.numberMatrix[1][0], self.m.numberMatrix[2][0])