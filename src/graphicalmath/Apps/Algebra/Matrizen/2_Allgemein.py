import pygame

from UIElements.AllUIElements import *
from WindowOverlayHelper.Window import Window
from UIElements.Matrix import Matrix, MatrixAnimation, MatrixAnimationTransponieren

class MatrizenAllgemein(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int):
        super().__init__(screen, x, y, z, width, height)

        # w: 1110, h: 800

        # === Main Window

        self.headline = Text(self.screen, 0, 0, 0, self.width, 100, "Matrix - Transponieren", fontSize=70, fontPath="assets/fonts/HEADLINE.ttf")
        self.headline.center = True
        self.addObject(self.headline)

        self.overall = Window(self.screen, 50, 100, 0, self.width - 100, 300)

        self.transponieren = Window(self.screen, 50, 115 + self.overall.height + 25, 0, self.width - 100, 390)

        self.addObject(self.overall)
        self.addObject(self.transponieren)

        o = lambda x: self.overall.addObject(x)
        p = lambda x: self.transponieren.addObject(x)

        # === Overall
        t = Text(self.screen, 0, 0, 0, self.overall.width / 3, 50, "Zeilenvektor (m = 1)", fontSize=25, fontPath="assets/fonts/Inter.ttf", center=True)
        t.font.bold = True
        o(t)
        self.zeilenVektor = Matrix(self.screen, 0, 50, 0, self.overall.width / 3, self.overall.height - 50)
        self.zeilenVektor.changeSize(1, 3)
        self.zeilenVektor.setCenter(True)
        o(self.zeilenVektor)

        t = Text(self.screen, self.zeilenVektor.width, 0, 0, self.overall.width / 3, 50, "Spaltenvektor (n = 1)", fontSize=25, fontPath="assets/fonts/Inter.ttf", center=True)
        t.font.bold = True
        o(t)
        self.spaltenVektor = Matrix(self.screen, self.zeilenVektor.width, 50, 0, self.overall.width / 3, self.overall.height - 50)
        self.spaltenVektor.changeSize(3, 1)
        self.spaltenVektor.setCenter(True)
        o(self.spaltenVektor)

        t = Text(self.screen, self.spaltenVektor.width * 2, 0, 0, self.overall.width / 3, 50, "quadratische Matrix (m = n)", fontSize=25, fontPath="assets/fonts/Inter.ttf", center=True)
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

        t = Text(self.screen, 0, 0, 0, 200, 50, "Transponieren", fontSize=25, fontPath="assets/fonts/Inter.ttf")
        t.font.bold = True
        p(t)

        self.inpMatrix = Matrix(self.screen, self.transponieren.width / 3, 65, 0, self.transponieren.width / 3, self.transponieren.height - 50)
        self.inpMatrix.changeSize(1, 1)
        p(self.inpMatrix)
        self.inpMatrix.setCenter(True)
        p(Text(self.screen, self.inpMatrix.x, 40, 0, self.inpMatrix.width, 25, "Input", fontSize=19, fontPath="assets/fonts/VeraMono.ttf", center=True))

        self.outMatrix = Matrix(self.screen, self.inpMatrix.width + self.inpMatrix.x, 65, 0, self.transponieren.width / 3, self.transponieren.height - 50)
        self.outMatrix.changeSize(3, 3)
        self.outMatrix.transponiert = True
        p(self.outMatrix)
        self.outMatrix.setCenter(True)
        self.outMatrix.lockTextBoxObjects(True)
        p(Text(self.screen, self.outMatrix.x, 40, 0, self.outMatrix.width, 25, "Output", fontSize=19, fontPath="assets/fonts/VeraMono.ttf", center=True))

        t1 = Text(self.screen, t.width,         0, 0, 40, 25, "m: 3", fontSize=17, fontPath="assets/fonts/VeraMono.ttf")
        s1 = Slider(self.screen, t.width + 40,  0, 0, 125, 19, onValueChange=lambda a, b: 
                   [self.inpMatrix.changeSize(m = int(a.value)), self.outMatrix.changeSize(n = int(a.value)), t1.setText("m: " + str(a.value))],
                   onValueChangeArgs=self.inpMatrix)
        s1.setMaxValue(4)
        s1.setMinValue(1)
        p(s1)
        p(t1)
        t2 = Text(self.screen, t.width,         25, 0, 40, 25, "n: 3", fontSize=17, fontPath="assets/fonts/VeraMono.ttf")
        s2 = Slider(self.screen, t.width + 40,  25, 0, 125, 19, onValueChange=lambda a, b: 
                   [self.inpMatrix.changeSize(n = int(a.value)), self.outMatrix.changeSize(m = int(a.value)), t2.setText("n: " + str(int(a.value)))],
                   onValueChangeArgs=self.inpMatrix)
        s2.setMaxValue(4)
        s2.setMinValue(1)
        p(s2)
        p(t2)

        animationWindow = Window(self.screen, 0, t.height + 10, 0, s1.x + s1.width, self.transponieren.height - t.height + 10)
        a = lambda x: animationWindow.addObject(x)
        # self.animationWindow.showColor = True
        # self.animationWindow.color = (255, 255, 255)
        p(animationWindow)

        self.animation = MatrixAnimationTransponieren(self.inpMatrix, self.outMatrix)
        a(self.animation)

        a(Button(self.screen, 0, 10, 0, 200, 35, text="Transponieren", onClick=lambda *args: self.animation.start()))
        a(Button(self.screen, 210, 10, 0, 200, 35, text="Stop", onClick=lambda *args: self.animation.stop()))
        t3 = Text(self.screen, 0, 85, 0, animationWindow.width, 25, "", fontSize=17, fontPath="assets/fonts/VeraMono.ttf", verticalCenter=True)
        s3 = Slider(self.screen, 150, 110, 0, animationWindow.width - 150, 19, 
                    onValueChange=lambda a, b: [self.animation.setSpeed(a.value / 10), t3.setText(f"Geschwindigkeit {round(a.value, 2)}: ")])
        s3.round = False
        s3.setMaxValue(3)
        s3.setMinValue(0.25)
        a(s3)
        a(t3)
        t4 = Text(self.screen, 0, 160, 0, animationWindow.width, 25, "", fontSize=17, fontPath="assets/fonts/VeraMono.ttf", verticalCenter=True)
        s4 = Slider(self.screen, 0, 185, 0, animationWindow.width, 19, 
                    onValueChange=lambda a, b: [self.animation.setFrame(int(a.value)), self.animation.setCurrentFramedt(int(a.value)),
                                                t4.setText(f"Frames {int(a.value) + 1} / {self.animation.totalFrames}: ")])
        self.animation.setFrameSlider(s4)
        a(s4)
        a(t4)

        a(Text(self.screen,      0, 235, 0, 100, 25, "Indizes: ", fontSize=20, fontPath="assets/fonts/VeraMono.ttf", verticalCenter=True))
        a(CheckBox(self.screen, 110, 235, 0,  25, 25, 
                     onClick=lambda a, b, c: [self.inpMatrix.setIndizesTextBox(a.value, Color.BLUE1), self.inpMatrix.lockTextBoxObjects(a.value),
                                              self.outMatrix.setIndizesTextBox(a.value, Color.BLUE1)]))
        a(MultiLineText(self.screen,      160, 235, 0, 200, 25, "(Output Indizes sind transponiert)", fontSize=14, fontPath="assets/fonts/VeraMono.ttf"))

        # === fill matrix
        w = 125
        h = 25
        matrixFillerWindow = Window(self.screen, self.width - w, 0, 0, w, 100)
        self.addObject(matrixFillerWindow)

        bFill = Button(self.screen, 0, h, 0, w, h, text="Fülle Matrix")
        bClear = Button(self.screen, 0, h * 2 + 10, 0, w, h, text="Reinige Matrix")

        for _ in [bFill, bClear]:
            matrixFillerWindow.addObject(_)

        bFill.onClick = lambda a, b, c: [self.inpMatrix.fillRandom()]
        bClear.onClick = lambda a, b, c: [self.inpMatrix.clear()]
     
module = MatrizenAllgemein