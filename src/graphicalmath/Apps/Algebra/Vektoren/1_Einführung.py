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

        uv1 = UIVector(self.screen, 250, 560, 0, 200, self.height - 560)
        uv1.coord = self.coord
        self.addObject(uv1)

        self.addObject(Text(self.screen, 50, 560, 0, 200, self.height - 560, "Vektor:", fontSize=20, center=True))
        self.addObject(Text(self.screen, 600, 560, 0, 250, 50, "Länge", fontSize=25, center=True))
        self.addObject(Text(self.screen, 600, 600, 0, 250, 50, "|Vektor| = √(x² + y² + z²)", fontSize=20, verticalCenter=True))
        t1 = Text(self.screen, 600, 650, 0, 500, 50, "|Vektor| = √(0² + 0² + 0²) = 0", fontSize=20, verticalCenter=True)
        self.addObject(t1)

        lenEvent = lambda x: t1.setText("|Vektor| = " + "".join([str(round(i, 2)) + " + " for i in uv1.getVector().toList()])[0:-2] + " = " +  str(round(uv1.getVector().length(), 2)))
        uv1.onChangeFunctions.append(lenEvent)

module = VektorEinführung