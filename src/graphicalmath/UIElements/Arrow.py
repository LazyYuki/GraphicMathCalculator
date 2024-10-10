import pygame

from WindowOverlayHelper.Window import Window
from EventManager.EventArgs import MouseEventArgs, KeyboardEventArgs
from UIElements.Rect import Rect

class Arrow(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int, orientation = "n", triangleLenForward = 0, triangleMargineSide = -1, color = (255, 255, 255)) -> None:
        super().__init__(screen, x, y, z, width, height)

        if orientation == "n" or orientation == "s":
            self.triangleHeight = height // 6 if triangleLenForward <= 0 else triangleLenForward
            self.triangleWidth = width

            triangleMargineSide = width // 3 if triangleMargineSide < 0 else triangleMargineSide

            if orientation == "n":
                self.rect = Rect(screen, triangleMargineSide, self.triangleHeight, z, 
                                 width - triangleMargineSide * 2, height - self.triangleHeight, color)
            else:
                self.rect = Rect(screen, triangleMargineSide, 0, z, 
                                 width - triangleMargineSide * 2, height - self.triangleHeight, color)

        elif orientation == "e" or orientation == "w":
            self.triangleHeight =  height
            self.triangleWidth = width // 6 if triangleLenForward <= 0 else triangleLenForward

            triangleMargineSide = height // 3 if triangleMargineSide < 0 else triangleMargineSide

            if orientation == "e":
                self.rect = Rect(screen, 0, triangleMargineSide, z, 
                                 width - self.triangleWidth, height - triangleMargineSide * 2, color)
            else:
                self.rect = Rect(screen, self.triangleWidth, triangleMargineSide, z, 
                                 width - self.triangleWidth, height - triangleMargineSide * 2, color)

        self.triangleMargineSide = triangleMargineSide

        self.color = color
        self.orientation = orientation

        self.addObject(self.rect)

        self.trianglePoints = []
        

    def changeBorderRadius(self, br: int):
        self.br_tr = br
        self.br_br = br
        self.br_tl = br
        self.br_bl = br

    def getTrianglePoints(self):
        if len(self.trianglePoints) != 0:
            return self.trianglePoints
        
        if self.orientation == "n":
            self.trianglePoints = [(self.realX + self.realWidth // 2, self.realY), 
                                   (self.realX, self.realY + self.triangleHeight), 
                                   (self.realX + self.realWidth, self.realY + self.triangleHeight)]
        elif self.orientation == "s":
            self.trianglePoints = [(self.realX + self.realWidth // 2, self.realY + self.realHeight), 
                                   (self.realX, self.realY + self.realHeight - self.triangleHeight), 
                                   (self.realX + self.realWidth, self.realY + self.realHeight - self.triangleHeight)]
        elif self.orientation == "e":
            self.trianglePoints = [(self.realX + self.realWidth, self.realY + self.realHeight // 2), 
                                   (self.realX + self.realWidth - self.triangleWidth, self.realY), 
                                   (self.realX + self.realWidth - self.triangleWidth, self.realY + self.realHeight)] 


        elif self.orientation == "w":
            self.trianglePoints = [(self.realX, self.realY + self.realHeight // 2), 
                                   (self.realX + self.triangleWidth, self.realY), 
                                   (self.realX + self.triangleWidth, self.realY + self.realHeight)]
            
        return self.trianglePoints


    def render(self):
        pygame.draw.polygon(self.screen, self.color, self.getTrianglePoints())
        
        super().render()