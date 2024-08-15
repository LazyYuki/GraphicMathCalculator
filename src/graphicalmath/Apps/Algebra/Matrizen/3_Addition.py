import pygame

from UIElements.AllUIElements import *
from WindowOverlayHelper.Window import Window
from UIElements.Matrix import Matrix, MatrixAnimation, MatrixAnimationTransponieren

class MatrizenAddition(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int):
        super().__init__(screen, x, y, z, width, height)

        # w: 1110, h: 800

        # === Main Window

        headline = Text(self.screen, 0, 0, 0, self.width, 100, "Matrix - Addition", fontSize=70, fontPath="assets/fonts/HEADLINE.ttf")
        headline.center = True
        self.addObject(headline)

        # === animation Window
        animationWindow = Window(self.screen, 50, 100, 0, self.width - 50, 100)
        self.addObject(animationWindow)

        tm = Text(self.screen, 0, 0, 0, 40, 25, "m: 3", fontSize=17, fontPath="assets/fonts/VeraMono.ttf", verticalCenter=True)
        sm = Slider(self.screen, 50, 0, 0, 150, 19)
        sm.setMaxValue(4)
        sm.setMinValue(1)
        tn = Text(self.screen, 0, 50, 0, 40, 25, "n: 3", fontSize=17, fontPath="assets/fonts/VeraMono.ttf", verticalCenter=True)
        sn = Slider(self.screen, 50, 50, 0, 150, 19)
        sn.setMaxValue(6)
        sn.setMinValue(1)

        bstart = Button(self.screen,    250, 0, 0, 110, 35, text="Start")
        bstop = Button(self.screen,     250, 50, 0, 110, 35, text="Stop")

        tspeed = Text(self.screen,      430, 0, 0, 210, 25, "Geschwindigkeit 1.00: ", fontSize=17, fontPath="assets/fonts/VeraMono.ttf", verticalCenter=True)
        sspeed = Slider(self.screen,    650, 0, 0, animationWindow.width - 700, 19)
        sspeed.round = False
        sspeed.setMaxValue(3)
        sspeed.setMinValue(0.25)
        tframes = Text(self.screen,     430, 50, 0, 210, 25, "Frames 10/10: ", fontSize=17, fontPath="assets/fonts/VeraMono.ttf", verticalCenter=True)
        sframes = Slider(self.screen,   650, 50, 0, animationWindow.width - 700, 19)

        for _ in [sm, tm, sn, tn, bstart, bstop, tspeed, sspeed, tframes, sframes]:
            animationWindow.addObject(_)

        # === input Window
        inputWindow = Window(self.screen, 50, animationWindow.y + animationWindow.height, 0, self.width - 50, (self.height - (animationWindow.y + animationWindow.height)) / 2)
        self.addObject(inputWindow)

        minp1 = Matrix(self.screen, 0, 0, 0,                        inputWindow.width / 2, inputWindow.height)
        minp2 = Matrix(self.screen, inputWindow.width / 2, 0, 0,    inputWindow.width / 2, inputWindow.height)
        minp1.setCenter(True)
        minp2.setCenter(True)
        minp1.changeSize(3, 3)
        minp2.changeSize(3, 3)
        toperator = Text(self.screen, 0, 0, 0, inputWindow.width, inputWindow.height, "+", fontSize=100, center=True)

        for _ in [minp1, minp2, toperator]:
            inputWindow.addObject(_)

        # === output Window
        outputWindow = Window(self.screen, 50, inputWindow.y + inputWindow.height, 0, self.width - 50, inputWindow.height)
        self.addObject(outputWindow)

        mout = Matrix(self.screen, 0, 0, 0, outputWindow.height, outputWindow.height)

        # === events
        sm.onValueChange = lambda a, b: [tm.setText(f"m: {int(sm.value)}"), minp1.changeSize(m = int(sm.value)), minp2.changeSize(m = int(sm.value))]
        sn.onValueChange = lambda a, b: [tn.setText(f"n: {int(sn.value)}"), minp1.changeSize(n = int(sn.value)), minp2.changeSize(n = int(sn.value))]


module = MatrizenAddition