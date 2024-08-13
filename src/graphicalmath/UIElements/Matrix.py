import pygame, copy, math, types

import pygame.freetype

from WindowOverlayHelper.Window import Window
from UIElements.AllUIElements import *
from EventManager.EventArgs import MouseEventArgs, KeyboardEventArgs

def mouseOnClick(self: TextBox, args):
    if self.clicked:
        return
    
    for i in range(len(self.parent.textBoxObjectMatrix)):
        for j in range(len(self.parent.textBoxObjectMatrix[i])):
            if self.parent.textBoxObjectMatrix[i][j] != self:
                self.parent.textBoxObjectMatrix[i][j].enter()

    self.clicked = True 
    self.styleRect.color = self.textBoxStyle.clickColor

    if self.text.text != "" and self.cursor == 0:
        self.setText("")

def textBoxOnChange(self: TextBox, args):
    pass

def textBoxOnEnter(self: TextBox, args):
    t = self.getText()

    t = ''.join(c for c in t if c.isdigit()).lstrip("0")

    if t == "":
        self.setText("0")
    else:
        self.setText(t)

    self.parent.numberMatrix[self.i][self.j] = int(self.getText())

class Matrix(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int) -> None:
        super().__init__(screen, x, y, z, width, height)
        
        self.numberMatrix = None
        self.m = 0
        self.n = 0

        self.textBoxObjectMatrix = None
        self.textBoxStyle = TextBoxStyles.matrix

        self.cellSize = 50
        self.outerPadding = 25
        self.innerPadding = 5

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

        bracket: Rect
        for bracket in [self.bracket1Top, self.bracket1Middle, self.bracket1Down, self.bracket2Top, self.bracket2Middle, self.bracket2Down]:
            self.addObject(bracket)

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

        # ==

        self.center = False

        self.calcShowRectPos()

    def setSizeFactor(self, newSizeFactor):
        if super().setSizeFactor(newSizeFactor):
            return True

        self.cellSize *= newSizeFactor
        self.outerPadding *= newSizeFactor
        self.innerPadding *= newSizeFactor

        self.changeSize(self.m, self.n)

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

        tmp_1 = min(self.m, self.n) * (self.cellSize + self.innerPadding)
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

        self.bracket1Middle.height = (self.cellSize + self.innerPadding) * self.m + self.outerPadding * 2 - self.innerPadding
        
        self.bracket1Down.y = self.bracket1Middle.height - self.bracket1Down.height
        self.bracket1Down.width = self.cellSize / 4 + self.outerPadding

        tmp = (self.cellSize + self.innerPadding) * self.n + self.outerPadding * 2 - self.innerPadding

        self.bracket2Top.x = tmp - self.bracket1Top.width + self.bracket2Middle.width
        self.bracket2Top.width = self.bracket1Top.width

        self.bracket2Middle.x = tmp 
        self.bracket2Middle.height = self.bracket1Middle.height

        self.bracket2Down.x = self.bracket2Top.x
        self.bracket2Down.y = self.bracket1Down.y
        self.bracket2Down.width = self.bracket1Down.width

        self.calcRealPosition()

    def changeSize(self, m = None, n = None):
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
            self.createTextBoxObjects()

        self.removeTextBoxObjects(m, n)
        
        self.m = m  
        self.n = n

        self.calcBracketPosition()
        self.setIndizesTextBox(self.showIndizes)
        self.lockTextBoxObjects(self.textBoxLocked)
        self.calcShowRectPos()
        
        self.setCenter(self.center)
        self.calcRealPosition()

    def createTextBoxObjects(self):
        for i in range(len(self.textBoxObjectMatrix)):
            for j in range(len(self.textBoxObjectMatrix[i])):
                if self.textBoxObjectMatrix[i][j] != None:
                    continue
                
                t = TextBox(self.screen,
                    self.outerPadding + (self.cellSize + self.innerPadding) * j, self.outerPadding + (self.cellSize + self.innerPadding) * i, 1, 
                    self.cellSize, self.cellSize, textBoxStyle=self.textBoxStyle)
                t.setText(str(self.numberMatrix[i][j]))
                t.i = i
                t.j = j
                t.onChangeText = types.MethodType(textBoxOnChange, t)
                t.onEnter = types.MethodType(textBoxOnEnter, t)
                t.mouseOnClick = types.MethodType(mouseOnClick, t)

                self.textBoxObjectMatrix[i][j] = t
                self.addObject(self.textBoxObjectMatrix[i][j])

    def removeTextBoxObjects(self, m, n):
        for i in range(len(self.textBoxObjectMatrix) - 1, -1, -1):
            for j in range(len(self.textBoxObjectMatrix[i]) - 1, -1, -1):
                if i >= m or j >= n:
                    self.removeObject(self.textBoxObjectMatrix[i][j])
                    self.textBoxObjectMatrix[i][j] = None

        for i in range(len(self.textBoxObjectMatrix)):
            self.textBoxObjectMatrix[i] = [j for j in self.textBoxObjectMatrix[i] if j is not None]

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

        for i in range(len(self.textBoxObjectMatrix)):
            for j in range(len(self.textBoxObjectMatrix[i])):
                self.textBoxObjectMatrix[i][j].setText(str(i + 1) + str(j + 1) if self.showIndizes else str(self.numberMatrix[i][j]))
                self.textBoxObjectMatrix[i][j].text.color = color if self.showIndizes else self.textBoxStyle.textColor

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
                    obj.x += cX
                    obj.y += cY

                    obj.matrixCenter = True

        else:
            for obj in self.objects:
                if obj.matrixCenter == True:
                    obj.x -= cX
                    obj.y -= cY

                    obj.matrixCenter = False

        self.calcRealPosition()

    def setEinheitsMatrix(self):
        for i in range(self.m):
            for j in range(self.n):
                if i == j:
                    self.numberMatrix[i][j] = 1
                else:
                    self.numberMatrix[i][j] = 0

    def render(self):
        if self.numberMatrix is None:
            return

        # for i in range(len(self.textBoxObjectMatrix)):
        #     for j in range(len(self.textBoxObjectMatrix[i])):
        #         self.textBoxObjectMatrix[i][j].render()

        super().render()