import pygame, copy, math, types

import pygame.freetype

from WindowOverlayHelper.Window import Window
from UIElements.AllUIElements import *
from EventManager.EventArgs import MouseEventArgs, KeyboardEventArgs

class Matrix(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int) -> None:
        super().__init__(screen, x, y, z, width, height)
        
        self.numberMatrix = None
        self.m = 0
        self.n = 0

        self.textBoxObjectMatrix = None
        self.textBoxStyle = TextBoxStyles.matrix

        self.cellSize = 50
        self.padding = 25

    def changeSize(self, m = None, n = None):
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
            self.textBoxObjectMatrix = [[None for _ in range(self.n)] for _ in range(m)]
        else:
            for i in range(m):
                if i >= len(self.textBoxObjectMatrix):
                    self.textBoxObjectMatrix.append([None for _ in range(n)])
                elif len(self.textBoxObjectMatrix[i]) < n:
                    self.textBoxObjectMatrix[i] += [None for _ in range(n - len(self.textBoxObjectMatrix[i]))]
                elif len(self.textBoxObjectMatrix[i]) > n:
                    self.textBoxObjectMatrix[i] = self.textBoxObjectMatrix[i][:n]

        if m > self.m:
            self.createTextBoxObjects(m, n)
        else:
            self.removeTextBoxObjects(m, n)
        
        self.m = m  
        self.n = n

    def createTextBoxObjects(self, m: int, n: int):
        for i in range(len(self.textBoxObjectMatrix), m):
            for j in range(len(self.textBoxObjectMatrix[i]), n):
                self.textBoxObjectMatrix[i][j] = TextBox(self.screen,
                    self.padding + self.cellSize * j, self.padding + self.cellSize * i, 0, self.cellSize, self.cellSize,
                    text=str(self.numberMatrix[i][j]), textBoxStyle=self.textBoxStyle)
                
                self.addObject(self.textBoxObjectMatrix[i][j])

    def removeTextBoxObjects(self, m: int, n: int):
        for i in range(m, len(self.textBoxObjectMatrix)):
            for j in range(self.n, len(self.textBoxObjectMatrix[i])):
                self.removeObject(self.textBoxObjectMatrix[i][j])
                self.textBoxObjectMatrix[i][j] = None

        for i in range(len(self.textBoxObjectMatrix)):
            self.textBoxObjectMatrix[i] = [j for j in self.textBoxObjectMatrix[i] if j is not None]

    def render(self):
        if self.numberMatrix is None:
            return

        super().render()