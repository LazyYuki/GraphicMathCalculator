import pygame
from pygame import gfxdraw  

from WindowOverlayHelper.WindowObject import WindowObject
from WindowOverlayHelper.Window import Window
from UIElements.Text import Text
from EventManager.EventArgs import MouseEventArgs, KeyboardEventArgs

class Sidebar(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int) -> None:
        """
        x y width height of total sidebar
        when closed, sidebar will be shown as circle in top left corner
        """
        super().__init__(screen, x, y, z, width, height)

        self.foregroundColor = (0, 0, 0)
        self.backgroundColor = (255, 255, 255)

        self.sidebarOpen = False
        self.closedCircleRadius = 35

        self.openWidth = width
        self.openHeight = height

        # self.content = Window(self.screen, x, y, z, width, height)

        # self.content.addObject(Text(screen, 0, 0, 0, 100, 20, "MATH", self.foregroundColor))

        # self.addObject(self.content)
        self.close()

    def close(self):
        self.sidebarOpen = False

        self.width = 2 * self.closedCircleRadius
        self.height = 2 * self.closedCircleRadius

        self.calcRealPosition()

    def open(self):
        self.sidebarOpen = True

        self.width = self.openWidth
        self.height = self.openHeight

        self.calcRealPosition()

    def mouseOnClick(self, args: MouseEventArgs):
        if self.sidebarOpen:
            self.close()
        else:
            self.open()

    def render(self):
        if self.sidebarOpen:
            pygame.draw.rect(self.screen, self.backgroundColor, 
                             rect=pygame.Rect(self.realX, self.realX, self.realWidth, self.realHeight), border_radius=20)
            # self.content.render()
        else:
            gfxdraw.filled_circle(self.screen, 
                               self.realX + self.closedCircleRadius, self.realY + self.closedCircleRadius, 
                               self.closedCircleRadius,
                               self.backgroundColor)
            pygame.draw.rect(self.screen, self.foregroundColor,
                             rect=pygame.Rect(self.realX + 0.25 * self.realWidth, 
                                              self.realY + 0.25 * self.realHeight, 
                                              0.5 * self.realWidth, 
                                              0.1 * self.realHeight), border_radius=20)
            pygame.draw.rect(self.screen, self.foregroundColor,
                             rect=pygame.Rect(self.realX + 0.25 * self.realWidth, 
                                              self.realY + 0.45 * self.realHeight, 
                                              0.5 * self.realWidth, 
                                              0.1 * self.realHeight), border_radius=20)
            pygame.draw.rect(self.screen, self.foregroundColor,
                             rect=pygame.Rect(self.realX + 0.25 * self.realWidth, 
                                              self.realY + 0.65 * self.realHeight, 
                                              0.5 * self.realWidth, 
                                              0.1 * self.realHeight), border_radius=20)
            
        # pygame.draw.rect(self.screen, (255, 0, 0), rect=pygame.Rect(self.realX, self.realX, self.realWidth, self.realHeight), width = 1)