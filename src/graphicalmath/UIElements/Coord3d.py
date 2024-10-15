import pygame

from WindowOverlayHelper.Window import Window
from EventManager.EventArgs import MouseEventArgs, KeyboardEventArgs
from UIElements.AllUIElements import *

SQRT2 = math.sqrt(2)

class Coord3d(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int) -> None:
        super().__init__(screen, x, y, z, width, height)

        # xAxis unit is halth of the units from y and z for 3d effect

        self.yAxis = rotatableArrow(screen, 0, height // 2, z, width, 20, 10, 3, 0, color=Color.WHITE)
        self.zAxis = rotatableArrow(screen, width // 2, height, z, height, 40, 10, 3, 90, color=Color.WHITE)

        l = width / SQRT2
        r = l / 2
        rad = math.radians(45)
        self.xAxis = rotatableArrow(screen, width/2 + math.cos(rad) * r, height / 2 - math.sin(rad) * r , z, l, 20, 10, 3, 225, color=Color.WHITE)

        for _ in [self.yAxis, self.zAxis, self.xAxis]:
            self.addObject(_)

        self.biggestNumberX = 5 #symmetrical
        self.biggestNumberY = 5
        self.biggestNumberZ = 5

        self.minDivisions = 10
        self.maxDivisions = 20

        self.texts = [[Text(screen, 0, 0, 0, 20, 20, center=True, fontPath="assets/fonts/VeraMono.ttf", fontSize=15) 
                       for _ in range(self.maxDivisions)] for _ in range(3)] #y = 0, z = 1, x = 2
        self.rects = [[Rect(screen, 0, 0, 0, 3, 10, color=Color.WHITE)
                       for _ in range(self.maxDivisions)] for _ in range(3)] #y = 0, z = 1, x = 2
        self.rectTextDistance = 5

        for _ in self.texts + self.rects:
            for __ in _:
                self.addObject(__)
                __.absoluteHide()

        self.setTextsY()

    def setTextsY(self):
        exponent = 0
        divisions = 0

        while True:
            divisions = (self.biggestNumberY * 2) / (2 ** exponent)

            if divisions < self.minDivisions:
                exponent -= 1
            elif divisions > self.maxDivisions:
                exponent += 1
            else:
                break
                
        d = self.yAxis.width / divisions

        for i in range(len(self.texts[0])):
            if i >= divisions:
                self.texts[0][i].absoluteHide()
                self.rects[0][i].absoluteHide()
                continue

            self.texts[0][i].center = True
            self.texts[0][i].x = self.yAxis.x + d * i - self.texts[0][i].width // 2
            self.texts[0][i].y = self.yAxis.y + self.rects[0][i].height // 2 + self.rectTextDistance
            self.texts[0][i].setText(str(-self.biggestNumberY + i * 2 ** exponent))
            self.texts[0][i].absoluteShow()

            self.rects[0][i].x = self.yAxis.x + d * i - self.rects[0][i].width // 2
            self.rects[0][i].y = self.yAxis.y - self.rects[0][i].height // 2
            self.rects[0][i].absoluteShow()

            