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

    def changeSize(self, m = None, n = None):
        print(m, n)

        if m == None:
            m = self.m
        if n == None:
            n = self.n

        if m < 1 or n < 1:
            return

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

        if self.textBoxObjectMatrix is None:
            self.textBoxObjectMatrix = [[None for _ in range(n)] for _ in range(m)]
        else:
            for i in range(m):
                if i >= len(self.textBoxObjectMatrix):
                    self.textBoxObjectMatrix.append([None for _ in range(n)])
                elif len(self.textBoxObjectMatrix[i]) < n:
                    self.textBoxObjectMatrix[i] += [None for _ in range(n - len(self.textBoxObjectMatrix[i]))]
                elif len(self.textBoxObjectMatrix[i]) > n:
                    self.textBoxObjectMatrix[i] = self.textBoxObjectMatrix[i][:n]

        if m > self.m:
            self.createTextBoxObjects()
        else:
            self.removeTextBoxObjects(m, n)
        
        self.m = m  
        self.n = n

    def createTextBoxObjects(self):
        for i in range(len(self.textBoxObjectMatrix)):
            for j in range(len(self.textBoxObjectMatrix[i])):
                if self.textBoxObjectMatrix[i][j] != None:
                    continue
                
                t = TextBox(self.screen,
                    self.outerPadding + (self.cellSize + self.innerPadding) * j, self.outerPadding + (self.cellSize + self.innerPadding) * i, 0, 
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
        for i in range(m, len(self.textBoxObjectMatrix)):
            for j in range(n, len(self.textBoxObjectMatrix[i])):
                self.removeObject(self.textBoxObjectMatrix[i][j])
                self.textBoxObjectMatrix[i][j] = None

        for i in range(len(self.textBoxObjectMatrix)):
            self.textBoxObjectMatrix[i] = [j for j in self.textBoxObjectMatrix[i] if j is not None]

    def render(self):
        if self.numberMatrix is None:
            return

        super().render()