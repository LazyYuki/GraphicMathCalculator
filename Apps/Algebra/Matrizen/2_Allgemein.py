import pygame

from UIElements.AllUIElements import *
from WindowOverlayHelper.Window import Window
from UIElements.Matrix import Matrix

class MatrizenAllgemein(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int):
        super().__init__(screen, x, y, z, width, height)

        # w: 1110, h: 800

        # === Main Window

        self.headline = Text(self.screen, 0, 0, 0, self.width, 100, "Matrix - Einfuehrung", fontSize=70, fontPath="Assets/Fonts/HEADLINE.ttf")
        self.headline.center = True
        self.addObject(self.headline)

        self.overall = Window(self.screen, 50, 100, 0, self.width - 100, 300)

        self.transponieren = Window(self.screen, 50, 115 + self.overall.height + 25, 0, self.width - 100, 390)

        self.addObject(self.overall)
        self.addObject(self.transponieren)

        o = lambda x: self.overall.addObject(x)
        p = lambda x: self.transponieren.addObject(x)

        # === Overall
        t = Text(self.screen, 0, 0, 0, self.overall.width / 3, 50, "Zeilenvektor (m = 1)", fontSize=25, fontPath="Assets/Fonts/Inter.ttf", center=True)
        t.font.bold = True
        o(t)
        self.zeilenVektor = Matrix(self.screen, 0, 50, 0, self.overall.width / 3, self.overall.height - 50)
        self.zeilenVektor.changeSize(1, 3)
        self.zeilenVektor.setCenter(True)
        o(self.zeilenVektor)

        t = Text(self.screen, self.zeilenVektor.width, 0, 0, self.overall.width / 3, 50, "Spaltenvektor (n = 1)", fontSize=25, fontPath="Assets/Fonts/Inter.ttf", center=True)
        t.font.bold = True
        o(t)
        self.spaltenVektor = Matrix(self.screen, self.zeilenVektor.width, 50, 0, self.overall.width / 3, self.overall.height - 50)
        self.spaltenVektor.changeSize(3, 1)
        self.spaltenVektor.setCenter(True)
        o(self.spaltenVektor)

        t = Text(self.screen, self.spaltenVektor.width * 2, 0, 0, self.overall.width / 3, 50, "quadratische Matrix (m = n)", fontSize=25, fontPath="Assets/Fonts/Inter.ttf", center=True)
        t.font.bold = True
        o(t)
        self.quadratischeMatrix = Matrix(self.screen, self.spaltenVektor.width * 2, 50, 0, self.overall.width / 3, self.overall.height - 50)
        self.quadratischeMatrix.changeSize(3, 3)
        self.quadratischeMatrix.setCenter(True)
        o(self.quadratischeMatrix)
        o(Button(self.screen, self.quadratischeMatrix.x + self.quadratischeMatrix.width / 2 - 150 / 2, self.overall.height - 40, 0, 
                 150, 35, text="Einheitsmatrix", 
                 onClick= lambda *args: [self.quadratischeMatrix.setEinheitsMatrix(), 
                                         self.quadratischeMatrix.setIndizesTextBox(False, self.quadratischeMatrix.textBoxStyle.textColor)]))
        
        # === Transponieren

        t = Text(self.screen, 0, 0, 0, 200, 50, "Transponieren", fontSize=25, fontPath="Assets/Fonts/Inter.ttf")
        t.font.bold = True
        p(t)

        self.inpMatrix = Matrix(self.screen, self.transponieren.width / 3, 65, 0, self.transponieren.width / 3, self.transponieren.height - 50)
        self.inpMatrix.changeSize(1, 1)
        p(self.inpMatrix)
        self.inpMatrix.setCenter(True)
        p(Text(self.screen, self.inpMatrix.x, 40, 0, self.inpMatrix.width, 25, "Input", fontSize=19, fontPath="Assets/Fonts/VeraMono.ttf", center=True))

        self.outMatrix = Matrix(self.screen, self.inpMatrix.width + self.inpMatrix.x, 65, 0, self.transponieren.width / 3, self.transponieren.height - 50)
        self.outMatrix.changeSize(3, 3)
        p(self.outMatrix)
        self.outMatrix.setCenter(True)
        self.outMatrix.lockTextBoxObjects(True)
        p(Text(self.screen, self.outMatrix.x, 40, 0, self.outMatrix.width, 25, "Output", fontSize=19, fontPath="Assets/Fonts/VeraMono.ttf", center=True))

        t1 = Text(self.screen, t.width,         0, 0, 40, 25, "m: 3", fontSize=17, fontPath="Assets/Fonts/VeraMono.ttf")
        s1 = Slider(self.screen, t.width + 40,  0, 0, 125, 19, onValueChange=lambda a, b: 
                   [self.inpMatrix.changeSize(m = int(a.value)), self.outMatrix.changeSize(n = int(a.value)), t1.setText("m: " + str(int(a.value)))],
                   onValueChangeArgs=self.inpMatrix)
        s1.setMaxValue(4)
        s1.setMinValue(1)
        p(s1)
        p(t1)
        t2 = Text(self.screen, t.width,         25, 0, 40, 25, "n: 3", fontSize=17, fontPath="Assets/Fonts/VeraMono.ttf")
        s2 = Slider(self.screen, t.width + 40,  25, 0, 125, 19, onValueChange=lambda a, b: 
                   [self.inpMatrix.changeSize(n = int(a.value)), self.outMatrix.changeSize(m = int(a.value)), t2.setText("n: " + str(int(a.value)))],
                   onValueChangeArgs=self.inpMatrix)
        s2.setMaxValue(4)
        s2.setMinValue(1)
        p(s2)
        p(t2)
     
module = MatrizenAllgemein