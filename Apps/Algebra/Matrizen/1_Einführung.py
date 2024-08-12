import pygame

from UIElements.AllUIElements import *
from UIElements.Matrix import Matrix
from WindowOverlayHelper.Window import Window

MATRIX_EINFUEHRUNGS_TEXT = "In der Mathematik versteht man unter einer Matrix (Plural Matrizen) eine rechteckige Anordnung (Tabelle) von Elementen (meist mathematischer Objekte, etwa Zahlen). Rechteckig bedeutet, dass die Anordnung der Elemente in Zeilen und Spalten stattfindet. Die Zeilen (m) und Spalten (n) einer Matrix nennt man zusammengefasst auch Reihen. "
MATRIX_TIPPS = "Tipp: Matrix Elemente können editiert werden, durch klicken auf das jeweilige Element und eingeben des neuen Wertes."

class MatrizenEinführung(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int):
        super().__init__(screen, x, y, z, width, height)

        # w: 1110, h: 800

        # === Main Window

        self.headline = Text(self.screen, 0, 0, 0, self.width, 100, "Matrix - Einfuehrung", fontSize=70, fontPath="Assets/Fonts/HEADLINE.ttf")
        self.headline.center = True

        self.explanation = MultiLineText(self.screen, 50, 115, 0, self.width - 100, 100, MATRIX_EINFUEHRUNGS_TEXT, fontSize=17, fontPath="Assets/Fonts/Inter.ttf")

        self.tipp = MultiLineText(self.screen, 50, 115 + self.explanation.height + 10, 0, self.width - 100, 100, MATRIX_TIPPS, fontSize=17, fontPath="Assets/Fonts/Inter.ttf")

        self.matrix = Matrix(self.screen, 550, 275, 0, 500, 500)
        self.matrix.changeSize(3, 3)

        self.addObject(self.headline)
        self.addObject(self.explanation)
        self.addObject(self.tipp)
        self.addObject(self.matrix)

        # === Interaction Window
        self.interactionWindow = Window(self.screen, 50, 275, 0, 500, 500)
        self.addObject(self.interactionWindow)
        add = lambda a: self.interactionWindow.addObject(a)

        tName = Text(self.screen, 0, 0, 0, self.interactionWindow.width, 25, f"Name: Matrix {self.matrix.m} x {self.matrix.n}", fontSize=20, fontPath="Assets/Fonts/VeraMono.ttf")
        tName.verticalCenter = True
        add(tName)

        t1 = Text(self.screen, 0, 30, 0, 100, 25, "m: ", fontSize=20, fontPath="Assets/Fonts/VeraMono.ttf")
        t1.verticalCenter = True
        add(t1)
        t2 = Text(self.screen, 0, 60, 0, 100, 25, "n: ", fontSize=20, fontPath="Assets/Fonts/VeraMono.ttf")
        t2.verticalCenter = True
        add(t2)

        s1 = Slider(self.screen, 100, 30, 0, 300, 25, onValueChange=lambda a, b: 
                   [self.matrix.changeSize(m = int(a.value)), t1.setText("m: " + str(int(a.value))), tName.setText("Name: Matrix " + str(b.m) + " x " + str(b.n))],
                   onValueChangeArgs=self.matrix)
        s1.setMaxValue(8)
        s1.setMinValue(1)
        add(s1)

        s2 = Slider(self.screen, 100, 60, 0, 300, 25, onValueChange=lambda a, b: 
                   [self.matrix.changeSize(n = int(a.value)), t2.setText("n: " + str(int(a.value))), tName.setText("Name: Matrix " + str(b.m) + " x " + str(b.n))],
                   onValueChangeArgs=self.matrix)
        s2.setMaxValue(8)
        s2.setMinValue(1)
        add(s2)

        add(Text(self.screen,      0, 150 + 30 * 0, 0, 225, 25, "Indizes: ", fontSize=20, fontPath="Assets/Fonts/VeraMono.ttf"))
        add(CheckBox(self.screen, 375, 150 + 30 * 0, 0,  25, 25, onClick=lambda a, b, c: [self.matrix.setIndizesTextBox(a.value, Color.BLUE1), self.matrix.lockTextBoxObjects(not a.value)]))

        add(Text(self.screen,      0, 150 + 30 * 1, 0, 225, 25, "Zeilen: ", fontSize=20, fontPath="Assets/Fonts/VeraMono.ttf"))
        add(CheckBox(self.screen, 375, 150 + 30 * 1, 0,  25, 25, onClick=lambda a, b, c: self.matrix.setShowRow(a.value), colorClicked=Color.RED))

        add(Text(self.screen,      0, 150 + 30 * 2, 0, 225, 25, "Spalte: ", fontSize=20, fontPath="Assets/Fonts/VeraMono.ttf"))
        add(CheckBox(self.screen, 375, 150 + 30 * 2, 0,  25, 25, onClick=lambda a, b, c: self.matrix.setShowColumn(a.value), colorClicked=Color.GREEN))

        add(Text(self.screen,      0, 150 + 30 * 3, 0, 225, 25, "Hauptdiagonale: ", fontSize=20, fontPath="Assets/Fonts/VeraMono.ttf"))
        add(CheckBox(self.screen, 375, 150 + 30 * 3, 0,  25, 25, onClick=lambda a, b, c: self.matrix.setShowMainDiagonal(a.value), colorClicked=Color.PURPLE))

        add(Text(self.screen,      0, 150 + 30 * 4, 0, 225, 25, "Gegendiagonale: ", fontSize=20, fontPath="Assets/Fonts/VeraMono.ttf"))
        add(CheckBox(self.screen, 375, 150 + 30 * 4, 0,  25, 25, onClick=lambda a, b, c: self.matrix.setShowAntiDiagonal(a.value), colorClicked=Color.YELLOW))

module = MatrizenEinführung