import pygame, copy, math, types, random

import pygame.freetype

from WindowOverlayHelper.Window import Window
from UIElements.AllUIElements import *
from EventManager.EventArgs import MouseEventArgs, KeyboardEventArgs

def mouseOnClick(self: TextBox, args):
    if self.clicked:
        return
    
    for i in range(self.parent.m):
        for j in range(self.parent.n):
            if self.parent.textBoxObjectMatrix[i][j] != self:
                self.parent.textBoxObjectMatrix[i][j].enter()

    self.clicked = True 
    self.styleRect.color = self.textBoxStyle.clickColor

    if self.text.text != "" and self.cursor == 0:
        self.setText("")

def textBoxOnChange(self: TextBox, args):
    pass

def textBoxOnEnter(self: TextBox, args):
    if self.i >= len(self.parent.numberMatrix) or self.j >= len(self.parent.numberMatrix[0]):
        return

    t = self.getText()

    t = ''.join(c for c in t if c.isdigit() or c in ["-", "."]).lstrip("0")

    if t == "":
        self.setText("0")
    else:
        self.setText(t)

    self.parent.numberMatrix[self.i][self.j] = round(float(self.getText()), 2)

    if self.parent.animation != None:
        self.parent.animation.reCalcFrames()
    
    if self.parent.nonUpdateAnimation != None:
        self.parent.nonUpdateAnimation.reCalcFrames()

    if self.parent.onTextBoxChange != None:
        self.parent.onTextBoxChange()

def setText(self: TextBox, text):
    if text.endswith(".0"):
        text = text[:-2]
    self.text.setText(text)
    self.cursor = len(text)

class MatrixAnimation(WindowObject):
    def __init__(self) -> types.NoneType:
        super().__init__(0, 0, 0, 0, 0, 0)

        self.currentFrame = 0
        self.currentFramedt = 0
        self.totalFrames = 0
        self.lastFrame = 0

        self.animationSpeed = 1 # animationFrames per sec

        self.frames = []

        self.run = False

        self.frameSlider = None

    def __del__(self):
        pass

    def setFrameSlider(self, slider: Slider):
        self.frameSlider = slider

        self.frameSlider.setMinValue(0)
        self.frameSlider.setMaxValue(self.lastFrame)

    def setSpeed(self, speed: int):
        self.animationSpeed = speed

    def start(self):
        self.run = True

        if self.currentFrame == self.lastFrame:
            self.currentFrame = 0
            self.currentFramedt = 0

            if self.frameSlider != None:
                self.frameSlider.setValue(self.currentFramedt)
            else:
                self.setFrame(self.currentFramedt)

    def stop(self):
        self.run = False

    def setCurrentFramedt(self, frame: int):
        self.currentFramedt = frame
        self.currentFrame = math.floor(self.currentFramedt)

    def update(self, dt: float):
        super().update(dt)

        if self.run:
            self.currentFramedt += self.animationSpeed * dt

            if math.floor(self.currentFramedt) == self.currentFrame:
                return
            
            self.currentFramedt = math.floor(self.currentFramedt)

            if self.currentFramedt >= self.lastFrame:
                self.currentFramedt = self.lastFrame
                self.run = False

            if self.frameSlider != None:
                self.frameSlider.setValue(self.currentFramedt)
            else:
                self.setFrame(self.currentFramedt)

    def reCalcFrames(self):
        """
        re calculate the frames
        """

        if self.frameSlider != None:
            self.frameSlider.setMinValue(0)
            self.frameSlider.setMaxValue(self.lastFrame)
            if self.frameSlider.onValueChange != None:
                self.frameSlider.onValueChange(self.frameSlider, self.frameSlider.onValueChangeArgs)


    def setFrame(self, frame: int):
        """
        set Matrix in correlation to the current Frame
        """

        self.currentFrame = frame

class Matrix(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int, innerPadding = (5, 5)) -> None:
        super().__init__(screen, x, y, z, width, height)
        
        self.numberMatrix = None
        self.m = 0
        self.n = 0

        self.textBoxObjectMatrix = None
        self.textBoxStyle = TextBoxStyles.matrix

        self.cellSize = 50
        self.outerPadding = 25
        # self.innerPadding = innerPadding

        self.innerPaddingX = innerPadding[0]
        self.innerPaddingY = innerPadding[1]

        # bracket
        size = 4

        self.bracket1Top = Rect(screen, 0, 0, 0, 25, size)
        self.bracket1Top.br_tr = 100
        self.bracket1Top.br_br = 100
        self.bracket1Middle = Rect(screen, 0, 0, 0, size, 25)
        self.bracket1Down = Rect(screen, 0, 0, 0, 25, size)
        self.bracket1Down.br_tr = 100
        self.bracket1Down.br_br = 100

        self.bracket2Top = Rect(screen, 0, 0, 0, 25, size)
        self.bracket2Top.br_tl = 100
        self.bracket2Top.br_bl = 100
        self.bracket2Middle = Rect(screen, 0, 0, 0, size, 25)
        self.bracket2Down = Rect(screen, 0, 0, 0, 25, size)
        self.bracket2Down.br_tl = 100
        self.bracket2Down.br_bl = 100

        brackets = [self.bracket1Top, self.bracket1Middle, self.bracket1Down, self.bracket2Top, self.bracket2Middle, self.bracket2Down]
        bracket: Rect
        for bracket in brackets:
            self.addObject(bracket)

        self.seperator = Rect(screen, 0, 0, 0, 0, 0, borderRadius=100)
        self.addObject(self.seperator)
        self.seperator.absoluteHide()

        self.calcBracketPosition()

        # special stuff
        self.showIndizes = False
        self.showRow = False
        self.showColumn = False
        self.showMainDiagonal = False
        self.showAntiDiagonal = False

        self.textBoxLocked = False

        self.showRowRect = Rect(screen, 0, 0, 0, 0, 0, color=Color.RED, borderRadius=15, borderWidth=3)
        self.showColumnRect = Rect(screen, 0, 0, 0, 0, 0, color=Color.GREEN, borderRadius=15, borderWidth=3)
        self.showMainDiagonalRect = RotatableRect(screen, 0, 0, 0, 0, 0, color=Color.PURPLE, borderRadius=15, borderWidth=3)
        self.showAntiDiagonalRect = RotatableRect(screen, 0, 0, 0, 0, 0, color=Color.YELLOW, borderRadius=15, borderWidth=3)

        show: Rect
        for show in [self.showRowRect, self.showColumnRect, self.showMainDiagonalRect, self.showAntiDiagonalRect]:
            self.addObject(show)
            show.absoluteHide()

        self.transponiert = False

        # == Center

        self.center = False
        self.xCenter = True
        self.yCenter = True

        self.calcShowRectPos()

        # == Animation
        self.animation: MatrixAnimation
        self.animation = None
        self.nonUpdateAnimation = None

        self.onTextBoxChange = None

    def calcShowRectPos(self):
        generaleSize = self.cellSize + self.outerPadding

        self.showRowRect.x = self.outerPadding / 2
        self.showRowRect.y = self.outerPadding / 2
        self.showRowRect.width = self.bracket2Middle.x - self.bracket1Middle.x - self.outerPadding
        self.showRowRect.height = generaleSize

        self.showColumnRect.x = self.outerPadding / 2
        self.showColumnRect.y = self.outerPadding / 2
        self.showColumnRect.width = generaleSize
        self.showColumnRect.height = self.bracket1Middle.height - self.outerPadding

        tmp_1 = min(self.m, self.n) * (self.cellSize + self.innerPaddingX)
        tmp_2 = min(self.bracket2Middle.x, self.bracket1Middle.height) / 2

        self.showMainDiagonalRect.x = 0
        self.showMainDiagonalRect.y = 0
        self.showMainDiagonalRect.setSize(
            generaleSize,
            math.sqrt(math.pow(tmp_1, 2) * 2)
        )
        self.showMainDiagonalRect.center = (tmp_2, tmp_2)
        self.showMainDiagonalRect.setAngle(45)

        self.showAntiDiagonalRect.x = 0
        self.showAntiDiagonalRect.y = 0
        self.showAntiDiagonalRect.setSize(
            generaleSize,
            math.sqrt(math.pow(tmp_1, 2) * 2)
        )
        self.showAntiDiagonalRect.center = (tmp_2, tmp_2 - 1)
        self.showAntiDiagonalRect.setAngle(-45)

        self.calcRealPosition()

    def calcBracketPosition(self):
        self.bracket1Top.width = self.cellSize / 4 + self.outerPadding

        self.bracket1Middle.height = (self.cellSize + self.innerPaddingY) * self.m + self.outerPadding * 2 - self.innerPaddingY
        
        self.bracket1Down.y = self.bracket1Middle.height - self.bracket1Down.height
        self.bracket1Down.width = self.cellSize / 4 + self.outerPadding

        tmp = (self.cellSize + self.innerPaddingX) * self.n + self.outerPadding * 2 - self.innerPaddingX

        self.bracket2Top.x = tmp - self.bracket1Top.width + self.bracket2Middle.width
        self.bracket2Top.width = self.bracket1Top.width

        self.bracket2Middle.x = tmp 
        self.bracket2Middle.height = self.bracket1Middle.height

        self.bracket2Down.x = self.bracket2Top.x
        self.bracket2Down.y = self.bracket1Down.y
        self.bracket2Down.width = self.bracket1Down.width

        self.seperator.x = (self.cellSize + self.innerPaddingX) * (self.n - 1) + self.outerPadding - self.innerPaddingX + self.innerPaddingX / 4
        self.seperator.y = self.outerPadding
        self.seperator.width = math.ceil(self.innerPaddingX / 2)
        self.seperator.height = self.bracket1Middle.height - self.outerPadding * 2

        self.calcRealPosition()

    def changeSize(self, m = None, n = None):
        for i in range(self.m):
            for j in range(self.n):
                if self.textBoxObjectMatrix[i][j].clicked:
                    self.textBoxObjectMatrix[i][j].enter()

        if m == None:
            m = self.m
        if n == None:
            n = self.n

        if m == self.m and n == self.n:
            return

        if m < 1 or n < 1:
            return
        
        tmp = self.center
        self.setCenter(False)
        self.center = tmp

        if self.numberMatrix is None:
            self.numberMatrix = [[0 for _ in range(n)] for _ in range(m)]
        else:
            for i in range(m):
                if i >= len(self.numberMatrix):
                    self.numberMatrix.append([0 for _ in range(n)])
                elif len(self.numberMatrix[i]) < n:
                    self.numberMatrix[i] += [0 for _ in range(n - len(self.numberMatrix[i]))]
                elif len(self.numberMatrix[i]) > n:
                    self.numberMatrix[i] = self.numberMatrix[i][:n]

            if m < len(self.numberMatrix):
                self.numberMatrix = self.numberMatrix[:m]

        if self.textBoxObjectMatrix is None:
            self.textBoxObjectMatrix = [[None for _ in range(n)] for _ in range(m)]
        else:
            for i in range(m):
                if i >= len(self.textBoxObjectMatrix):
                    self.textBoxObjectMatrix.append([None for _ in range(n)])
                elif len(self.textBoxObjectMatrix[i]) < n:
                    self.textBoxObjectMatrix[i] += [None for _ in range(n - len(self.textBoxObjectMatrix[i]))]

        if m > self.m or n > self.n:
            self.createTextBoxObjects(m, n)

        self.removeTextBoxObjects(m, n)
        
        self.m = m  
        self.n = n

        self.calcBracketPosition()
        self.setIndizesTextBox(self.showIndizes)
        self.lockTextBoxObjects(self.textBoxLocked)
        self.calcShowRectPos()
        
        self.setCenter(self.center)
        self.calcRealPosition()

        if self.animation != None:
            self.animation.reCalcFrames()
            self.animation.setFrame(0)

    def createTextBoxObjects(self, m, n):
        for i in range(m):
            for j in range(n):
                if self.textBoxObjectMatrix[i][j] != None:
                    self.textBoxObjectMatrix[i][j].lockEvents = False
                    self.textBoxObjectMatrix[i][j].absoluteShow()
                    self.textBoxObjectMatrix[i][j].setText(str(self.numberMatrix[i][j]))
                    continue
                
                t = TextBox(self.screen,
                    self.outerPadding + (self.cellSize + self.innerPaddingX) * j, self.outerPadding + (self.cellSize + self.innerPaddingY) * i, 1, 
                    self.cellSize, self.cellSize, textBoxStyle=self.textBoxStyle)
                t.setText(str(self.numberMatrix[i][j]))
                t.i = i
                t.j = j
                t.onChangeText = types.MethodType(textBoxOnChange, t)
                t.onEnter = types.MethodType(textBoxOnEnter, t)
                t.mouseOnClick = types.MethodType(mouseOnClick, t)
                t.setText = types.MethodType(setText, t)

                self.textBoxObjectMatrix[i][j] = t
                self.addObject(self.textBoxObjectMatrix[i][j])

    def removeTextBoxObjects(self, m, n):
        for i in range(len(self.textBoxObjectMatrix) - 1, -1, -1):
            for j in range(len(self.textBoxObjectMatrix[i]) - 1, -1, -1):
                if i >= m or j >= n:
                    # self.removeObject(self.textBoxObjectMatrix[i][j])
                    # self.textBoxObjectMatrix[i][j] = None

                    self.textBoxObjectMatrix[i][j].absoluteHide()
                    self.textBoxObjectMatrix[i][j].lockEvents = True

    def lockTextBoxObjects(self, lock = None):
        if lock == None:
            lock = self.textBoxLocked
            self.textBoxLocked = not self.textBoxLocked
        else:
            self.textBoxLocked = lock

        v = not lock

        for i in range(len(self.textBoxObjectMatrix)):
            for j in range(len(self.textBoxObjectMatrix[i])):
                self.textBoxObjectMatrix[i][j].lockEvents = not v
                self.textBoxObjectMatrix[i][j].events = v

                self.textBoxObjectMatrix[i][j].clicked = False

    def setIndizesTextBox(self, show = None, color = None):
        if show == None:
            show = self.showIndizes
            self.showIndizes = not self.showIndizes
        else:
            self.showIndizes = show

        if color == None:
            color = Color.BLUE1

        for i in range(self.m):
            for j in range(self.n):
                if self.transponiert:
                    self.textBoxObjectMatrix[i][j].setText(str(j + 1) + str(i + 1) if self.showIndizes else str(self.numberMatrix[i][j]))
                else:
                    self.textBoxObjectMatrix[i][j].setText(str(i + 1) + str(j + 1) if self.showIndizes else str(self.numberMatrix[i][j]))
                self.textBoxObjectMatrix[i][j].text.color = color if self.showIndizes else self.textBoxStyle.textColor

    def setNumberMatrix(self):
        if len(self.numberMatrix) != self.m or len(self.numberMatrix[0]) != self.n:
            return
        
        if self.showIndizes:
            return 

        for i in range(self.m):
            for j in range(self.n):
                self.textBoxObjectMatrix[i][j].setText(str(self.numberMatrix[i][j]))

    def setShowMainDiagonal(self, v):
        self.showMainDiagonal = v

        if self.showMainDiagonal:
            self.showMainDiagonalRect.absoluteShow()
        else:
            self.showMainDiagonalRect.absoluteHide()

    def setShowRow(self, v):
        self.showRow = v

        if self.showRow:
            self.showRowRect.absoluteShow()
        else:
            self.showRowRect.absoluteHide()

    def setShowColumn(self, v):
        self.showColumn = v

        if self.showColumn:
            self.showColumnRect.absoluteShow()
        else:
            self.showColumnRect.absoluteHide()

    def setShowAntiDiagonal(self, v):
        self.showAntiDiagonal = v

        if self.showAntiDiagonal:
            self.showAntiDiagonalRect.absoluteShow()
        else:
            self.showAntiDiagonalRect.absoluteHide()

    def setCenter(self, c: bool):
        self.center = c

        self.calcRealPosition()

        cX = (self.realWidth - (self.bracket2Middle.x - self.bracket1Middle.x)) / 2
        cY = (self.realHeight - self.bracket1Middle.height) / 2

        if self.center:
            for obj in self.objects:
                if obj.matrixCenter == False:
                    if self.xCenter: obj.x += cX
                    if self.yCenter: obj.y += cY

                    obj.matrixCenter = True

        else:
            for obj in self.objects:
                if obj.matrixCenter == True:
                    if self.xCenter: obj.x -= cX
                    if self.yCenter: obj.y -= cY

                    obj.matrixCenter = False

        self.calcRealPosition()

    def setEinheitsMatrix(self):
        for i in range(self.m):
            for j in range(self.n):
                if i == j:
                    self.numberMatrix[i][j] = 1
                else:
                    self.numberMatrix[i][j] = 0

    def setPointerToIndex(self, pointer: Rect, x, y, w = -1, h = -1):
        pointer.x = self.outerPadding + (self.cellSize + self.innerPaddingX) * x + self.cellSize / 2 - (pointer.width if w == -1 else w) / 2
        pointer.y = self.outerPadding + (self.cellSize + self.innerPaddingY) * y + self.cellSize / 2 - (pointer.height if h == -1 else h) / 2
        pointer.matrixCenter = False

        self.setCenter(self.center)
        self.calcRealPosition()

    def fillRandom(self, min = -10, max = 10):
        for i in range(self.m):
            for j in range(self.n):
                self.numberMatrix[i][j] = random.randint(min, max)

        self.setNumberMatrix()

        if self.animation != None:
            self.animation.reCalcFrames()
            self.animation.setFrame(0)

    def hideBreakets(self):
        for bracket in [self.bracket1Top, self.bracket1Middle, self.bracket1Down, self.bracket2Top, self.bracket2Middle, self.bracket2Down]:
            bracket.absoluteHide()

    def showBreakets(self):
        for bracket in [self.bracket1Top, self.bracket1Middle, self.bracket1Down, self.bracket2Top, self.bracket2Middle, self.bracket2Down]:
            bracket.absoluteShow()

    def showSeperator(self):
        self.seperator.absoluteShow()

    def hideSeperator(self):
        self.seperator.absoluteHide()

    def clear(self):
        for i in range(self.m):
            for j in range(self.n):
                self.numberMatrix[i][j] = 0

        self.setNumberMatrix()

        if self.animation != None:
            self.animation.reCalcFrames()
            self.animation.setFrame(0)

    def render(self):
        if self.numberMatrix is None:
            return

        # for i in range(len(self.textBoxObjectMatrix)):
        #     for j in range(len(self.textBoxObjectMatrix[i])):
        #         self.textBoxObjectMatrix[i][j].render()

        super().render()

class MatrixAnimationTransponieren(MatrixAnimation):
    def __init__(self, m1: Matrix, m2: Matrix) -> None:
        super().__init__()

        self.m1 = m1
        self.m2 = m2

        self.m1.animation = self

        size1 = m1.cellSize + m1.innerPaddingX / 2
        size2 = m2.cellSize + m2.innerPaddingX / 2
        self.pointer1 = Rect(m1.screen, 0, 0, 0, size1, size1, color=Color.RED, borderRadius=15, borderWidth=3)
        self.pointer2 = Rect(m2.screen, 0, 0, 0, size2, size2, color=Color.RED, borderRadius=15, borderWidth=3)

        m1.addObject(self.pointer1)
        m2.addObject(self.pointer2)

        for x in [self.pointer1, self.pointer2]:
            x.absoluteHide()

        self.reCalcFrames()

        # frame = (m2.numberMatrix, (p1.x, p1.y), (p2.x, p2.y), showPointer)

    def __del__(self):
        self.m1.removeObject(self.pointer1)
        self.m2.removeObject(self.pointer2)

    def reCalcFrames(self):
        self.frames = [([[0 for _ in range(self.m1.m)] for _ in range(self.m1.n)], (0, 0), (0, 0), False)]

        transponiert = [[0 for _ in range(self.m1.m)] for _ in range(self.m1.n)]
        for i in range(self.m1.m):
            for j in range(self.m1.n):
                transponiert[j][i] = self.m1.numberMatrix[i][j]

                self.frames.append((copy.deepcopy(transponiert), (j, i), (i, j), True))

        self.frames.append((copy.deepcopy(transponiert), (0, 0), (0, 0), False))

        self.totalFrames = len(self.frames)
        self.lastFrame = self.totalFrames - 1
        self.currentFrame = min(self.currentFrame, self.lastFrame)

        super().reCalcFrames()

    def setFrame(self, frame: int):
        if frame == self.currentFrame:
            return

        if frame >= self.totalFrames and frame < 0:
            return

        f = self.frames[frame]

        self.m2.numberMatrix = f[0]
        self.m2.setNumberMatrix()

        self.m1.setPointerToIndex(self.pointer1, f[1][0], f[1][1])
        self.m2.setPointerToIndex(self.pointer2, f[2][0], f[2][1])

        if f[3]:
            self.pointer1.absoluteShow()
            self.pointer2.absoluteShow()
        else:
            self.pointer1.absoluteHide()
            self.pointer2.absoluteHide()

        super().setFrame(frame)

class MatrixAnimationAddition(MatrixAnimation):
    def __init__(self, m1: Matrix, m2: Matrix, m3: Matrix, text: Text) -> None:
        super().__init__()

        # m1 = m2 + m3

        self.m1 = m1
        self.m2 = m2
        self.m3 = m3
        self.text = text

        self.m1.animation = self
        self.m2.animation = self
        self.m3.animation = self

        size = m1.cellSize + m1.innerPaddingX / 2

        self.pointer1 = Rect(m1.screen, 0, 0, 0, size, size, color=Color.GREEN, borderRadius=15, borderWidth=3)
        self.pointer2 = Rect(m2.screen, 0, 0, 0, size, size, color=Color.RED, borderRadius=15, borderWidth=3)
        self.pointer3 = Rect(m3.screen, 0, 0, 0, size, size, color=Color.RED, borderRadius=15, borderWidth=3)

        m1.addObject(self.pointer1)
        m2.addObject(self.pointer2)
        m3.addObject(self.pointer3)

        for x in [self.pointer1, self.pointer2, self.pointer3]:
            x.absoluteHide()

        self.reCalcFrames()

        # frame = (m2.numberMatrix, (p1.x, p1.y), (p2.x, p2.y), showPointer)

    def __del__(self):
        self.m1.removeObject(self.pointer1)
        self.m2.removeObject(self.pointer2)
        self.m3.removeObject(self.pointer3)

    def reCalcFrames(self):
        self.frames = [([[0 for _ in range(self.m1.n)] for _ in range(self.m1.m)], (0, 0), False, "", "")]

        if self.m1.m != self.m2.m or self.m1.n != self.m2.n or self.m2.m != self.m3.m or self.m2.n != self.m3.n:
            self.totalFrames = len(self.frames)
            self.lastFrame = self.totalFrames - 1
            self.currentFrame = min(self.currentFrame, self.lastFrame)
            return

        addiert = [[0 for _ in range(self.m1.n)] for _ in range(self.m1.m)]
        for i in range(self.m1.m):
            for j in range(self.m1.n):
                addiert[i][j] = self.m2.numberMatrix[i][j] + self.m3.numberMatrix[i][j]

                self.frames.append((copy.deepcopy(addiert), (i, j), True, f"{i, j}:    ", f"{self.m2.numberMatrix[i][j]} + {self.m3.numberMatrix[i][j]} = {addiert[i][j]}"))

        self.frames.append((copy.deepcopy(addiert), (0, 0), False, "", ""))

        self.totalFrames = len(self.frames)
        self.lastFrame = self.totalFrames - 1
        self.currentFrame = min(self.currentFrame, self.lastFrame)

        super().reCalcFrames()

    def setFrame(self, frame: int):
        if frame == self.currentFrame:
            return

        if frame >= self.totalFrames and frame < 0:
            return

        f = self.frames[frame]

        self.m1.numberMatrix = f[0]
        self.m1.setNumberMatrix()

        self.m1.setPointerToIndex(self.pointer1, f[1][1], f[1][0])
        self.m2.setPointerToIndex(self.pointer2, f[1][1], f[1][0])
        self.m3.setPointerToIndex(self.pointer3, f[1][1], f[1][0])

        self.text.setText(f[3] + f[4])

        if f[2]:
            self.pointer1.absoluteShow()
            self.pointer2.absoluteShow()
            self.pointer3.absoluteShow()
        else:
            self.pointer1.absoluteHide()
            self.pointer2.absoluteHide()
            self.pointer3.absoluteHide()

        super().setFrame(frame)

class MatrixAnimationMult(MatrixAnimation):
    def __init__(self, m1: Matrix, m2: Matrix, m3: Matrix, letterRenderer: LetterRenderer) -> None:
        super().__init__()

        # m1 * m2 = m3

        self.m1 = m1
        self.m2 = m2
        self.m3 = m3
        self.letterRenderer = letterRenderer

        self.m1.animation = self
        self.m2.animation = self
        self.m3.animation = self

        self.size = m1.cellSize + m1.innerPaddingX / 2

        self.pointer1 = Rect(m1.screen, 0, 0, 0, m1.showRowRect.width, self.size, color=Color.YELLOW, borderRadius=15, borderWidth=3)
        self.pointer2 = Rect(m2.screen, 0, 0, 0, self.size, m2.showColumnRect.height, color=Color.PURPLE, borderRadius=15, borderWidth=3)
        self.pointer3 = Rect(m3.screen, 0, 0, 0, self.size, self.size, color=Color.GREEN, borderRadius=15, borderWidth=3)

        m1.addObject(self.pointer1)
        m2.addObject(self.pointer2)
        m3.addObject(self.pointer3)

        for x in [self.pointer1, self.pointer2, self.pointer3]:
            x.absoluteHide()

        self.reCalcFrames()

        # frame = (m2.numberMatrix, (p1.x, p1.y), (p2.x, p2.y), showPointer)

    def __del__(self):
        self.m1.removeObject(self.pointer1)
        self.m2.removeObject(self.pointer2)
        self.m3.removeObject(self.pointer3)

    def reCalcFrames(self):
        self.frames = [([[0 for _ in range(self.m3.n)] for _ in range(self.m3.m)], (0, 0), (0, 0), (0, 0), False, [])]

        self.pointer1.width = self.size  + (self.m1.cellSize + self.m1.innerPaddingX) * (self.m1.n - 1)
        self.pointer2.height = self.size + (self.m1.cellSize + self.m1.innerPaddingX) * (self.m2.m - 1)

        if self.m1.n != self.m2.m or self.m1.m != self.m3.m or self.m2.n != self.m3.n:
            self.totalFrames = len(self.frames)
            self.lastFrame = self.totalFrames - 1
            self.currentFrame = min(self.currentFrame, self.lastFrame)
            return

        mult = [[0 for _ in range(self.m3.n)] for _ in range(self.m3.m)]

        for i in range(self.m3.m):
            for j in range(self.m3.n):
                letterText = []
                w = 0

                for k in range(self.m1.n):
                    mult[i][j] += self.m1.numberMatrix[i][k] * self.m2.numberMatrix[k][j]

                    w = max(w, len(str(self.m1.numberMatrix[i][k])), len(str(self.m2.numberMatrix[k][j])))

                    letterText.append([str(self.m1.numberMatrix[i][k]), Color.YELLOW])
                    letterText.append([" * ", Color.WHITE])
                    letterText.append([str(self.m2.numberMatrix[k][j]), Color.PURPLE])
                    letterText.append([" + \n", Color.WHITE])
 
                for t in range(0, len(letterText)):
                    if letterText[t][0] == " + \n" or letterText[t][0] == " * ":
                        continue

                    letterText[t][0] = letterText[t][0].rjust(w, " ")

                letterText.pop()
                letterText.append(["\n = ", Color.WHITE])
                letterText.append([str(mult[i][j]), Color.GREEN])

                self.frames.append((copy.deepcopy(mult), (i, 0), (0, j), (i, j),  True, letterText))

        self.frames.append((mult, (0, 0), (0, 0), (0, 0), False, []))

        self.totalFrames = len(self.frames)
        self.lastFrame = self.totalFrames - 1
        self.currentFrame = min(self.currentFrame, self.lastFrame)

        super().reCalcFrames()

    def setFrame(self, frame: int):
        if frame == self.currentFrame:
            return

        if frame >= self.totalFrames and frame < 0:
            return

        f = self.frames[frame]

        self.m3.numberMatrix = f[0]
        self.m3.setNumberMatrix()

        self.m1.setPointerToIndex(self.pointer1, f[1][1], f[1][0], self.size, self.size)
        self.m2.setPointerToIndex(self.pointer2, f[2][1], f[2][0], self.size, self.size)
        self.m3.setPointerToIndex(self.pointer3, f[3][1], f[3][0])

        self.letterRenderer.setText(f[5])

        if f[4]:
            self.pointer1.absoluteShow()
            self.pointer2.absoluteShow()
            self.pointer3.absoluteShow()
        else:
            self.pointer1.absoluteHide()
            self.pointer2.absoluteHide()
            self.pointer3.absoluteHide()

        super().setFrame(frame)

class MatrixAnimationGauß(MatrixAnimation):
    def __init__(self, m1: Matrix, mList: list, lrList: list) -> None:
        super().__init__()

        # m1 * m2 = m3

        self.m1 = m1
        self.mList = mList
        self.lrList = lrList

        self.m1.animation = self

        self.size = self.mList[0].cellSize + self.mList[0].innerPaddingX / 2

        self.pList = []

        self.mStartFrame = [0, 0, 0, 0, 0, 0]

        for i in range(len(mList)):
            pointer = Rect(m1.screen, 0, 0, 0, m1.showRowRect.width, self.size, color=Color.random(), borderRadius=15, borderWidth=3)
            self.pList.append(pointer)
            self.mList[i].addObject(pointer)
            pointer.absoluteHide()

        self.reCalcFrames()

        # frame = (m2.numberMatrix, (p1.x, p1.y), (p2.x, p2.y), showPointer)

    def __del__(self):
        for i in range(len(self.mList)):
            self.mList[i].removeObject(self.pList[i])

    def reCalcFrames(self):
        self.mFrames = [[[[[0] for _ in range(self.m1.n)] for _ in range(self.m1.m)]] for _ in range(6)]
        self.mFrames[0][0] = copy.deepcopy(self.m1.numberMatrix)

        self.pFrames = [[[0, 0, False]] for _ in range(5)]

        self.lrFrames = [[[]] for _ in range(10)]
        # self.lrFrames.append([])

        # Frame 1
        f = 1

        i = 0

        x1 = self.mList[0].numberMatrix[0][0]
        x2 = self.mList[0].numberMatrix[1][0]
        x3 = self.mList[0].numberMatrix[2][0]

        e1 = - x2 / x1
        e2 = - x3 / x1

        self.mFrames[1] = copy.deepcopy(self.m1.numberMatrix)
        self.lrFrames[f][0] = [["- ", Color.WHITE], [str(x2), self.pList[i + 1].color], [" / ", Color.WHITE], [str(x1), self.pList[i].color], [" = ", Color.WHITE], [str(e1),  Color.WHITE]]
        self.lrFrames[f][1] = [["- ", Color.WHITE], [str(x3), self.pList[i + 2].color], [" / ", Color.WHITE], [str(x1), self.pList[i].color], [" = ", Color.WHITE], [str(e2),  Color.WHITE]]

        self.pFrames[0].append((0, 0, False))

        # Frame 2
        f = 2

        self.lrFrames[f][0] = [["- ", Color.WHITE], [str(x2), Color.WHITE], [" / ", Color.WHITE], [str(x1), Color.WHITE], [" = ", Color.WHITE], [str(e1),  self.pList[i + 1].color]]
        self.lrFrames[f][1] = [["- ", Color.WHITE], [str(x3), Color.WHITE], [" / ", Color.WHITE], [str(x1), Color.WHITE], [" = ", Color.WHITE], [str(e2),  self.pList[i + 2].color]]


        # for i in range(2):
        #     self.pFrames[i].append([0, 0, True])
        #     self.pFrames[i + 1].append([1, 0, True])
        #     self.pFrames[i + 2].append([2, 0, True])

        #     for j in range(i + 2, len(self.pFrames)):
        #         self.pFrames[j].append([0, 0, False])
            
        #     for j in range(i * 2, len(self.lrFrames)):
        #         self.lrFrames[j].append([])

        #     x1 = self.mList[i].numberMatrix[0][0]
        #     x2 = self.mList[i].numberMatrix[1][0]
        #     x3 = self.mList[i].numberMatrix[2][0]

        #     if x1 == 0:
        #         return

        #     y2 = - x2 / x1
        #     y3 = - x3 / x1

        #     self.lrFrames[i].append([["- ", Color.WHITE], [str(x2), self.pList[i + 1].color], [" / ", Color.WHITE], [str(x1), self.pList[i].color], [" = ", Color.WHITE], [str(y2), self.pList[i + 1].color]])
        #     self.lrFrames[i + 1].append([["- ", Color.WHITE], [str(x3), self.pList[i + 2].color], [" / ", Color.WHITE], [str(x1), self.pList[i].color], [" = ", Color.WHITE], [str(y3), self.pList[i + 2].color]])

            


        self.totalFrames = len(self.frames)
        self.lastFrame = self.totalFrames - 1
        self.currentFrame = min(self.currentFrame, self.lastFrame)

        super().reCalcFrames()

    def setFrame(self, frame: int):
        if frame == self.currentFrame:
            return

        if frame >= self.totalFrames and frame < 0:
            return

        f = self.frames[frame]

        self.m3.numberMatrix = f[0]
        self.m3.setNumberMatrix()

        self.m1.setPointerToIndex(self.pointer1, f[1][1], f[1][0], self.size, self.size)
        self.m2.setPointerToIndex(self.pointer2, f[2][1], f[2][0], self.size, self.size)
        self.m3.setPointerToIndex(self.pointer3, f[3][1], f[3][0])

        self.letterRenderer.setText(f[5])

        if f[4]:
            self.pointer1.absoluteShow()
            self.pointer2.absoluteShow()
            self.pointer3.absoluteShow()
        else:
            self.pointer1.absoluteHide()
            self.pointer2.absoluteHide()
            self.pointer3.absoluteHide()

        super().setFrame(frame)