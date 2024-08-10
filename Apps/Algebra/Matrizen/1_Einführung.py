import pygame

from UIElements.AllUIElements import *
from UIElements.Matrix import Matrix
from WindowOverlayHelper.Window import Window

class MatrizenEinführung(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int):
        super().__init__(screen, x, y, z, width, height)

        self.headline = Text(self.screen, 0, 0, 0, self.width, 100, "Matrix - Einfuehrung", fontSize=70, fontPath="Assets/Fonts/HEADLINE.ttf")
        self.headline.center = True

        self.matrix = Matrix(self.screen, 450, 200, 0, 600, 600)
        self.matrix.changeSize(3, 3)

        t1 = Text(self.screen, 10, 200, 0, 100, 25, "m: ", fontSize=20, fontPath="Assets/Fonts/VeraMono.ttf")
        t1.verticalCenter = True
        self.addObject(t1)
        t2 = Text(self.screen, 10, 230, 0, 100, 25, "n: ", fontSize=20, fontPath="Assets/Fonts/VeraMono.ttf")
        t2.verticalCenter = True
        self.addObject(t2)

        s = Slider(self.screen, 120, 200, 0, 200, 25, onValueChange=lambda a, b: [self.matrix.changeSize(m = int(a.value)), t1.setText("m: " + str(int(a.value)))])
        s.setMaxValue(8)
        s.setMinValue(1)
        self.addObject(s)

        f = Slider(self.screen, 120, 230, 0, 200, 25, onValueChange=lambda a, b: [self.matrix.changeSize(n = int(a.value)), t2.setText("n: " + str(int(a.value)))])
        f.setMaxValue(8)
        f.setMinValue(1)
        self.addObject(f)

        self.addObject(self.headline)
        self.addObject(self.matrix)

        self.addObject(Text(self.screen,      10, 280 + 30 * 0, 0, 225, 25, "Indizes: ", fontSize=20, fontPath="Assets/Fonts/VeraMono.ttf"))
        self.addObject(CheckBox(self.screen, 235, 280 + 30 * 0, 0,  25, 25, onClick=lambda a, b, c: [self.matrix.lockTextBoxObjects(not a.value), self.matrix.setIndizesTextBox(a.value)]))

        self.addObject(Text(self.screen,      10, 280 + 30 * 1, 0, 225, 25, "Reihe: ", fontSize=20, fontPath="Assets/Fonts/VeraMono.ttf"))
        self.addObject(CheckBox(self.screen, 235, 280 + 30 * 1, 0,  25, 25, onClick=lambda a, b, c: self.matrix.setRow(a.value)))

        self.addObject(Text(self.screen,      10, 280 + 30 * 2, 0, 225, 25, "Spalte: ", fontSize=20, fontPath="Assets/Fonts/VeraMono.ttf"))
        self.addObject(CheckBox(self.screen, 235, 280 + 30 * 2, 0,  25, 25, onClick=lambda a, b, c: self.matrix.setColumn(a.value)))

        self.addObject(Text(self.screen,      10, 280 + 30 * 3, 0, 225, 25, "Hauptdiagonale: ", fontSize=20, fontPath="Assets/Fonts/VeraMono.ttf"))
        self.addObject(CheckBox(self.screen, 235, 280 + 30 * 3, 0,  25, 25, onClick=lambda a, b, c: self.matrix.setMainDiagonal(a.value)))

        self.addObject(Text(self.screen,      10, 280 + 30 * 4, 0, 225, 25, "Gegendiagonale: ", fontSize=20, fontPath="Assets/Fonts/VeraMono.ttf"))
        self.addObject(CheckBox(self.screen, 235, 280 + 30 * 4, 0,  25, 25, onClick=lambda a, b, c: self.matrix.setAntiDiagonal(a.value)))

module = MatrizenEinführung