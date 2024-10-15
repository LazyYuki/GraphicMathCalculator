import pygame

from UIElements.AllUIElements import *
from WindowOverlayHelper.Window import Window
from UIElements.Matrix import Matrix, MatrixAnimationMult

def gleichungszeile(screen, x, y, cellsize = 50, margin = 10):
    componentsTextbox = []
    componentsText = []

    tW = 50

    for i in range(3):
        componentsTextbox.append(TextBox(screen, x + (cellsize + margin) * i * 2, y, 0, cellsize, cellsize, textBoxStyle=TextBoxStyles.matrix))
        componentsText.append(Text(screen, x + (cellsize + margin) * i * 2 + cellsize, y, 0, tW, cellsize, ("a +", "b +", "c =")[i], fontSize=TextBoxStyles.matrix.fontSize, fontPath=TextBoxStyles.matrix.fontPath, center=True))

    componentsTextbox.append(TextBox(screen, x + (cellsize + margin) * i, y, 0, cellsize, cellsize, textBoxStyle=TextBoxStyles.matrix))

    return componentsTextbox, componentsText

class MatrixGauß(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int):
        super().__init__(screen, x, y, z, width, height)

        # w: 1110, h: 800

        # === Main Window

        headline = Text(self.screen, 0, 0, 0, self.width, 100, "Matrix - Gauss", fontSize=70, fontPath="assets/fonts/HEADLINE.ttf")
        headline.center = True
        self.addObject(headline)

        wAnimationControl = Window(self.screen, 0, 100, 0, self.width, 80)
        # wAnimationControl.debug((255, 0, 0))
        wScroll = ScrollWindow(self.screen, 0, 0, 2, self.width, self.height * 2)
        wScroll.scrollSpeed = 20
        wScroll.maxScroll = 180
        wScroll.minScroll = -1000
        wScroll.overrightRealHeight = self.height * 2
        # wScroll.debug((0, 255, 0))

        for _ in [wAnimationControl, wScroll]:
            self.addObject(_)

        # === Animation Control
        awW = wAnimationControl.width

        bstart = Button(self.screen,    0, 0, 0, 110, 35, text="Start")
        bstop = Button(self.screen,     0, 40, 0, 110, 35, text="Stop")
        tspeed = Text(self.screen,      140, 0, 0, 210, 35, "Geschw. 0.25: ", fontSize=17, fontPath="assets/fonts/VeraMono.ttf", verticalCenter=True)
        sspeed = Slider(self.screen,    300, 8, 0, awW - 300, 19)
        sspeed.round = False
        tframes = Text(self.screen,     140, 40, 0, 210, 35, "Frames 10/10: ", fontSize=17, fontPath="assets/fonts/VeraMono.ttf", verticalCenter=True)
        sframes = Slider(self.screen,   300, 48, 0, awW - 300, 19)
        sframes.onlyEventItemInForeground = True

        for _ in [bstart, bstop, tspeed, sspeed, tframes, sframes]:
            wAnimationControl.addObject(_)


        # === Hauptteil

        # Text
        uwW = wScroll.width

        wScroll.addObject(MultiLineText(self.screen, 5, 20, 0, uwW, 110, " • Lösung von Gleichungssystemen\n • erste a: a ≠ 0 (Pivotelement)"))

        # Input
        mInp = Matrix(self.screen, 20, 110, 0, 500, 300, (50, 5))
        mInp.hideBreakets()
        mInp.changeSize(3, 4)

        x = mInp.x + mInp.outerPadding + mInp.cellSize * 0.7
        y = mInp.y + mInp.outerPadding
        for i in range(3):
            for j in range(3):
                _ = Text(self.screen, x + (mInp.cellSize + mInp.innerPaddingX) * j, y + (mInp.cellSize + mInp.innerPaddingY) * i, 0, 
                                       mInp.cellSize, mInp.cellSize, ("a +", "b +", "c =")[j] + str(i + 1), fontSize=21, fontPath="assets/fonts/VeraMono.ttf", center=True)
                _.font.bold  = True
                wScroll.addObject(_)

        t1 = Text(self.screen, mInp.x, mInp.y - 20, 0, mInp.bracket2Middle.x - mInp.x, 40, "Gleichungssystem", fontSize=25, fontPath="assets/fonts/VeraMono.ttf", center=True)
        t1.font.bold = True
        wScroll.addObject(Arrow(self.screen, mInp.bracket2Middle.x, t1.y + 10, 0, 300, 20, orientation="e"))

        for _ in [mInp, t1]:
            wScroll.addObject(_)

        # = animationMatrix
        mOutList = []
        lrList = []

        for i in range(6):
            m = Matrix(self.screen, 600, i * 250, 0, 500, 250)
            m.setCenter(True)
            m.changeSize(3, 4)
            m.lockTextBoxObjects(True)
            m.showSeperator()
            mOutList.append(m)
            wScroll.addObject(m)
            wScroll.addObject(Text(self.screen, m.x + 450, m.y, 0, 200, m.height, str(i + 1), fontSize=70, fontPath="assets/fonts/VeraMono.ttf", verticalCenter=True))

            if i == 3:
                wScroll.addObject(Rect(self.screen, 0, m.y - 3, 0, wScroll.width, 6, color=Color.YELLOW))
                wScroll.addObject(Text(self.screen, 0, m.y - 30, 0, wScroll.width, 30, "Gauß-Algorithmus zu Ende", fontSize=17, fontPath="assets/fonts/VeraMono.ttf", verticalCenter=True, color=Color.YELLOW))
                wScroll.addObject(Text(self.screen, 0, m.y, 0, wScroll.width, 30, "Gauß-Jordan-Algorithmus beginnt", fontSize=17, fontPath="assets/fonts/VeraMono.ttf", verticalCenter=True, color=Color.YELLOW))
 
            if i != 0:
                # = Rechnung
                wRechnung1 = Window(self.screen, m.x - 200, m.y + m.bracket1Top.y + m.outerPadding + (m.cellSize + m.innerPaddingY) * 1, 0, 300, m.cellSize)
                wRechnung2 = Window(self.screen, m.x - 200, m.y + m.bracket1Top.y + m.outerPadding + (m.cellSize + m.innerPaddingY) * 2, 0, 300, m.cellSize)
                
                for a in [wRechnung1, wRechnung2]:
                    a.addObject(Arrow(self.screen, 200, m.cellSize / 2 - 8, 0, 75, 16, orientation="e"))
                    a.addObject(Text(self.screen, 275, 0, 0, 25, m.cellSize, center=True, text="+", fontPath="assets/fonts/VeraMono.ttf", fontSize=25))
                    lr = LetterRenderer(self.screen, 0, 12, 0, 200, 25, fontSize=25, fontPath="assets/fonts/VeraMono.ttf")
                    
                    lrList.append(lr)
                    a.addObject(lr)

                wScroll.addObject(wRechnung1)
                wScroll.addObject(wRechnung2)

        # === scroll trixen
        self.addObject(Rect(self.screen, 0, 0, 1, self.width, 180, color=(0,0,0)))
        wScroll.setScroll(180)
        wScroll.realHeight = self.height * 2

        # === fill matrix
        w = 125
        h = 25
        matrixFillerWindow = Window(self.screen, self.width - w, 0, 0, w, 100)
        self.addObject(matrixFillerWindow)

        bFill = Button(self.screen, 0, h, 0, w, h, text="Fülle Matrix")
        bClear = Button(self.screen, 0, h * 2 + 10, 0, w, h, text="Reinige Matrix")

        for _ in [bFill, bClear]:
            matrixFillerWindow.addObject(_)

        bFill.onClick = lambda a, b, c: [mInp.fillRandom()]
        bClear.onClick = lambda a, b, c: [mInp.clear()]

module = MatrixGauß