import pygame

from WindowOverlayHelper.Window import Window
from EventManager.EventArgs import MouseEventArgs, KeyboardEventArgs
from UIElements.AllUIElements import *
from UIElements.Matrix import *

from math_calc.Vector import Vector3d

class UIVector(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int) -> None:
        super().__init__(screen, x, y, z, width, height)

        self.m = Matrix(self.screen, 0, 0, 0, self.width, self.height)
        self.m.setCenter(True)
        self.m.changeSize(3, 1)
        self.m.onTextBoxChange = self.matrixChange

        self.addObject(self.m)

        self.__v = None

        self.coord = None

        self.onChangeFunctions = []

    def matrixChange(self, *args):
        if self.coord != None:
            if self.__v != None:
                self.coord.removeVector(self.__v)
                
            self.coord.addVector(self._getCoordVector())
            self.coord.renderMatplotLib()
        else:
            self._getCoordVector()

        for f in self.onChangeFunctions:
            f(self)

    def _getCoordVector(self):
        self.__v = self.getVector()
        return self.__v

    def getVector(self):
        return Vector3d(self.m.numberMatrix[0][0], self.m.numberMatrix[1][0], self.m.numberMatrix[2][0])