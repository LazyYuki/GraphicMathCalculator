import pygame

from UIElements.AllUIElements import *
from WindowOverlayHelper.Window import Window
from UIElements.Matrix import Matrix, MatrixAnimationAddition

class MatrixMultiplikation(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int):
        super().__init__(screen, x, y, z, width, height)

        # w: 1110, h: 800

        # === Main Window

        headline = Text(self.screen, 0, 0, 0, self.width, 100, "Matrix - Multiplikation", fontSize=70, fontPath="assets/fonts/HEADLINE.ttf")
        headline.center = True
        self.addObject(headline)

        y = 100
        h = (self.height - 100) / 2
        x = self.width - h - 100

        matrixWindowInp2 = Window(self.screen, x + 50, y,     0, h, h)
        matrixWindowInp1 = Window(self.screen, x - h + 50, y + h, 0, h, h)
        matrixWindowOut3 = Window(self.screen, x + 50, y + h, 0, h, h)

        berechnungsWindow = Window(self.screen, 0, y + h + 50, 0, x - h, h - 100)
        # berechnungsWindow.showColor = True
        # berechnungsWindow.color = (255, 0, 0)

        animationWindow = Window(self.screen,  0,       y, 0, x, 75)
        # animationWindow.showColor = True
        # animationWindow.color = (0, 255, 0)

        utilityWindow = Window(self.screen, 0, y + animationWindow.height + 30, 0, x, h - animationWindow.height - 30)
        # utilityWindow.showColor = True
        # utilityWindow.color = (0, 0, 255)

        for _ in [matrixWindowInp2, matrixWindowInp1, matrixWindowOut3, berechnungsWindow, animationWindow, utilityWindow]:
            self.addObject(_)

        # === matrix
        minp1 = Matrix(self.screen, 0, 0, 0, matrixWindowInp1.width, matrixWindowInp1.height)
        minp2 = Matrix(self.screen, 0, 0, 0, matrixWindowInp2.width, matrixWindowInp2.height)
        mout = Matrix(self.screen, 0, 0, 0, matrixWindowOut3.width, matrixWindowOut3.height)

        minp1.setCenter(True)
        minp2.setCenter(True)
        mout.setCenter(True)

        minp1.changeSize(4, 4)
        minp2.changeSize(4, 4)
        mout.changeSize(4, 4)

        matrixWindowInp1.addObject(minp1)
        matrixWindowInp2.addObject(minp2)
        matrixWindowOut3.addObject(mout)

        
        # === animation Window

        awW = animationWindow.width

        bstart = Button(self.screen,    0, 0, 0, 110, 35, text="Start")
        bstop = Button(self.screen,     0, 40, 0, 110, 35, text="Stop")
        tspeed = Text(self.screen,      140, 0, 0, 210, 35, "Geschw. 0.25: ", fontSize=17, fontPath="assets/fonts/VeraMono.ttf", verticalCenter=True)
        sspeed = Slider(self.screen,    300, 8, 0, awW - 300, 19)
        sspeed.round = False
        tframes = Text(self.screen,     140, 40, 0, 210, 35, "Frames 10/10: ", fontSize=17, fontPath="assets/fonts/VeraMono.ttf", verticalCenter=True)
        sframes = Slider(self.screen,   300, 48, 0, awW - 300, 19)

        for _ in [bstart, bstop, tspeed, sspeed, tframes, sframes]:
            animationWindow.addObject(_)

        # === utility Window

        uwW = utilityWindow.width
        z = 20

        t1 = MultiLineText(self.screen, 0, z, 0, uwW, utilityWindow.height, " • Gegeben sind 2 Matrizen A und B.\n • m(A) muss n(B) entsprechen.\n • (A und B sind nicht tauschbar)\n • A * B = C")
        t2 = Text(self.screen, uwW - 230, z, 0, uwW, t1.height, "Visualisierung:", fontSize=20, fontPath="assets/fonts/VeraMono.ttf", verticalCenter=True)
        c1 = CheckBox(self.screen, uwW - 30, (t1.height) / 2 + z - 12.5, 0, 25, 25)
        t3 = Text(self.screen, uwW - 260, z + 30, 0, uwW, t1.height, "Gleiche Farben sind gleich groß", fontSize=13, fontPath="assets/fonts/VeraMono.ttf", verticalCenter=True)

        for _ in [t1, t2, c1, t3]:
            utilityWindow.addObject(_)

        # Visualisierung

        m = 45

        aBn = Arrow(self.screen, m, 20, 0, h - m * 2, 25, orientation="e", color=(255, 0, 255))
        tBn = Text(self.screen, aBn.x, aBn.y + aBn.height, 0, aBn.width, aBn.height, "n(B)", center=True, color=aBn.color, fontSize=25)
        aBm = Arrow(self.screen, 20, m, 0, 25, h - m * 2, orientation="s", color=(0, 255, 255))
        tBm = Text(self.screen, aBm.x + aBm.width, aBm.y, 0, 60, aBm.height, "m(B)", center=True, color=aBm.color, fontSize=25)
        tB = Text(self.screen, 0, 0, 0, h, h, "B", fontSize=150, fontPath="assets/fonts/VeraMono.ttf", center=True, color=(100, 100, 100))

        for _ in [aBn, aBm, tB, tBn, tBm]:
            matrixWindowInp2.addObject(_)

        aAn = Arrow(self.screen, m, 20, 0, h - m * 2, 25, orientation="e", color=(0, 255, 255))
        tAn = Text(self.screen, aAn.x, aAn.y + aAn.height, 0, aAn.width, aAn.height, "n(A)", center=True, color=aAn.color, fontSize=25)
        aAm = Arrow(self.screen, 20, m, 0, 25, h - m * 2, orientation="s", color=(255, 255, 0))
        tAm = Text(self.screen, aAm.x + aAm.width, aAm.y, 0, 60, aAm.height, "m(A)", center=True, color=aAm.color, fontSize=25)
        tA = Text(self.screen, 0, 0, 0, h, h, "A", fontSize=150, fontPath="assets/fonts/VeraMono.ttf", center=True, color=(100, 100, 100))

        for _ in [aAn, aAm, tA, tAn, tAm]:
            matrixWindowInp1.addObject(_)

        aCn = Arrow(self.screen, m, 20, 0, h - m * 2, 25, orientation="e", color=(255, 0, 255))
        tCn = Text(self.screen, aCn.x, aCn.y + aCn.height, 0, aCn.width, aCn.height, "n(C)", center=True, color=aCn.color, fontSize=25)
        aCm = Arrow(self.screen, 20, m, 0, 25, h - m * 2, orientation="s", color=(255, 255, 0))
        tCm = Text(self.screen, aCm.x + aCm.width, aCm.y, 0, 60, aCm.height, "m(C)", center=True, color=aCm.color, fontSize=25)
        tC = Text(self.screen, 0, 0, 0, h, h, "C", fontSize=150, fontPath="assets/fonts/VeraMono.ttf", center=True, color=(100, 100, 100))

        for _ in [aCn, aCm, tC, tCn, tCm]:
            matrixWindowOut3.addObject(_)

        visualisierung = [aAn, aAm, tA, tAn, tAm, aBn, aBm, tB, tBn, tBm, aCn, aCm, tC, tCn, tCm]
        showVisualisierung = lambda: [_.absoluteShow() for _ in visualisierung]
        hideVisualisierung = lambda: [_.absoluteHide() for _ in visualisierung]
        hideVisualisierung()

        # slider

        utilitySliderWindow = Window(self.screen, 0, t1.height + t1.y + 30, 0, utilityWindow.width, utilityWindow.height - t1.height - t1.y - 60)
        utilityWindow.addObject(utilitySliderWindow)

        sliderW = utilitySliderWindow.width / 2 - 125

        sAm = Slider(self.screen, 80,   3, 0, sliderW, 19)
        stAm = Text(self.screen, 0,      0, 0, 100, 25, "m(A): 1", fontSize=17, fontPath="assets/fonts/VeraMono.ttf", verticalCenter=True)
        sAn = Slider(self.screen, 80,  33, 0, sliderW, 19)
        stAn = Text(self.screen, 0,     30, 0, 100, 25, "n(A): 1", fontSize=17, fontPath="assets/fonts/VeraMono.ttf", verticalCenter=True)

        sBm = Slider(self.screen, sliderW + 180,     3, 0, sliderW, 19)
        stBm = Text(self.screen, sliderW + 100,            0, 0, 100, 25, "m(B): 1", fontSize=17, fontPath="assets/fonts/VeraMono.ttf", verticalCenter=True)
        sBn = Slider(self.screen, sliderW + 180,    33, 0, sliderW, 19)
        stBn = Text(self.screen, sliderW + 100,           30, 0, 100, 25, "n(B): 1", fontSize=17, fontPath="assets/fonts/VeraMono.ttf", verticalCenter=True)

        for _ in [sAm, stAm, sAn, stAn, sBm, stBm, sBn, stBn]:
            utilitySliderWindow.addObject(_)

        # === berechnungs Window

        tbw = Text(self.screen, 0, 5, 0, berechnungsWindow.width - 5, 25, "Berechnungsschritt", fontSize=25, center=True)
        tbw.font.bold = True

        lrbw = LetterRenderer(self.screen, 5, 40, 0, berechnungsWindow.width - 5, berechnungsWindow.height - 40 * 2, fontSize=20)
        
        for _ in [tbw, lrbw]:
            berechnungsWindow.addObject(_)

        # === events
        c1.onClick = lambda a, b, c: [showVisualisierung() if c1.value else hideVisualisierung()]

        sAm.onValueChange = lambda a, b: [stAm.setText(f"m(A): {int(sAm.value)}"), minp1.changeSize(m = int(sAm.value)), mout.changeSize(m = int(sAm.value))]
        sAn.onValueChange = lambda a, b: [stAn.setText(f"n(A): {int(sAn.value)}"), sBm.setValue(int(sAn.value)), minp1.changeSize(n = int(sAn.value))]
        sBm.onValueChange = lambda a, b: [stBm.setText(f"m(B): {int(sBm.value)}"), sAn.setValue(int(sBm.value)), minp2.changeSize(m = int(sAn.value))]
        sBn.onValueChange = lambda a, b: [stBn.setText(f"n(B): {int(sBn.value)}"), minp2.changeSize(n = int(sBn.value)), mout.changeSize(n = int(sBn.value))]

        # animation = MatrixAnimationAddition(mout, minp1, minp2, calcLogWindow)
        # outputWindow.addObject(animation)
        
        # bstart.onClickArg = animation
        # bstop.onClickArg = animation
        # bstart.onClick = lambda y, x, z: x.start()
        # bstop.onClick = lambda y, x, z: x.stop()

        # === start up
        for _ in [sAm, sAn, sBm, sBn]:
            _.setMaxValue(4)
            _.setMinValue(1)

module = MatrixMultiplikation