import pygame

from UIElements.AllUIElements import *
from WindowOverlayHelper.Window import Window
from UIElements.Matrix import Matrix, MatrixAnimationAddition

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

        tm = Text(self.screen, 0, 0, 0, 40, 25, "m: 1", fontSize=17, fontPath="assets/fonts/VeraMono.ttf", verticalCenter=True)
        sm = Slider(self.screen, 50, 0, 0, 150, 19)
        tn = Text(self.screen, 0, 50, 0, 40, 25, "n: 1", fontSize=17, fontPath="assets/fonts/VeraMono.ttf", verticalCenter=True)
        sn = Slider(self.screen, 50, 50, 0, 150, 19)
        

        bstart = Button(self.screen,    250, 0, 0, 110, 35, text="Start")
        bstop = Button(self.screen,     250, 50, 0, 110, 35, text="Stop")

        tspeed = Text(self.screen,      430, 0, 0, 210, 25, "Geschwindigkeit 0.25: ", fontSize=17, fontPath="assets/fonts/VeraMono.ttf", verticalCenter=True)
        sspeed = Slider(self.screen,    650, 0, 0, animationWindow.width - 700, 19)
        sspeed.round = False
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
        minp1.changeSize(1, 1)
        minp2.changeSize(1, 1)
        toperator = Text(self.screen, 0, 0, 0, inputWindow.width, inputWindow.height, "+", fontSize=100, center=True)

        for _ in [minp1, minp2, toperator]:
            inputWindow.addObject(_)

        # === output Window
        outputWindow = Window(self.screen, 50, inputWindow.y + inputWindow.height, 0, self.width - 100, inputWindow.height)
        self.addObject(outputWindow)
        
        outputWindow.addObject(Text(self.screen, 0, 0, 0, outputWindow.width / 5, inputWindow.height, "=", fontSize=100, center=True))

        mout = Matrix(self.screen, outputWindow.width / 5, 0, 0, outputWindow.width, outputWindow.height)
        mout.changeSize(1, 1)
        mout.xCenter = False
        mout.setCenter(True)
        mout.lockTextBoxObjects(True)

        outputWindow.addObject(mout)

        calcLogWindow = ScrollWindow(self.screen, outputWindow.width / 5 * 3, 0, 0, outputWindow.width / 5 * 2, outputWindow.height)
        calcLogWindow.scrollSpeed = 20
        calcLogWindow.minScroll = 0
        calcLogWindow.maxScroll = 0
        outputWindow.addObject(calcLogWindow)

        outputWindow.addObject(Rect(self.screen, calcLogWindow.x, calcLogWindow.y, 0, calcLogWindow.width, calcLogWindow.height, color=Color.BLUE1, borderRadius=25, borderWidth=2))

        t1 = Text(self.screen, 0, 5, 0, calcLogWindow.width, 25, "Berechnungsschritt", fontSize=25, center=True)
        t1.font.bold = True
        calcLogWindow.addObject(t1)

        t2 = Text(self.screen, 0, 50, 0, calcLogWindow.width, 25, "", fontSize=20, center=True)
        calcLogWindow.addObject(t2)

        # === animation Matrix
        animation = MatrixAnimationAddition(mout, minp1, minp2, t2)
        outputWindow.addObject(animation)
        
        bstart.onClickArg = animation
        bstop.onClickArg = animation
        bstart.onClick = lambda y, x, z: x.start()
        bstop.onClick = lambda y, x, z: x.stop()

        # === events
        sm.onValueChange = lambda a, b: [tm.setText(f"m: {int(sm.value)}"), minp1.changeSize(m = int(sm.value)), minp2.changeSize(m = int(sm.value)), mout.changeSize(m = int(sm.value))]
        sn.onValueChange = lambda a, b: [tn.setText(f"n: {int(sn.value)}"), minp1.changeSize(n = int(sn.value)), minp2.changeSize(n = int(sn.value)), mout.changeSize(n = int(sn.value))]

        sspeed.onValueChange = lambda a, b: [animation.setSpeed(sspeed.value / 5), tspeed.setText(f"Geschwindigkeit {sspeed.value:.2f}: ")]
        sframes.onValueChange = lambda a, b: [animation.setFrame(int(a.value)), animation.setCurrentFramedt(int(a.value)), tframes.setText(f"Frames {int(sframes.value) + 1}/{animation.totalFrames}: ")]

        # === start up
        sn.setMaxValue(6)
        sn.setMinValue(1)
        sm.setMaxValue(4)
        sm.setMinValue(1)
        sspeed.setMaxValue(10)
        sspeed.setMinValue(0.5)
        sspeed.setValue(2.00)
        animation.setFrameSlider(sframes)

        # === fill matrix
        w = 125
        h = 25
        matrixFillerWindow = Window(self.screen, self.width - w, 0, 0, w, 100)
        self.addObject(matrixFillerWindow)

        bFill = Button(self.screen, 0, h, 0, w, h, text="Fülle Matrix")
        bClear = Button(self.screen, 0, h * 2 + 10, 0, w, h, text="Reinige Matrix")

        for _ in [bFill, bClear]:
            matrixFillerWindow.addObject(_)

        bFill.onClick = lambda a, b, c: [minp1.fillRandom(), minp2.fillRandom()]
        bClear.onClick = lambda a, b, c: [minp1.clear(), minp2.clear()]


module = MatrizenAddition