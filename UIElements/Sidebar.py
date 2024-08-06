import pygame
from pygame import gfxdraw  

from WindowOverlayHelper.WindowObject import WindowObject
from WindowOverlayHelper.Window import Window
from UIElements.Text import Text
from UIElements.TextBox import TextBox
from UIElements.Rect import Rect
from EventManager.EventArgs import MouseEventArgs, KeyboardEventArgs
from Application.Color import *

class Sidebar(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int, 
                 closedSidebarWidth = 50, openSidebarWidth = 300 ) -> None:
        """
        x y width height of total sidebar
        when closed, sidebar will be shown as circle in top left corner
        """
        super().__init__(screen, x, y, z, width, height)

        self.foregroundColor = Color.BLACK
        self.backgroundColor = Color.WHITE

        self.sidebarOpen = False
        self.closedSidebarWidth = closedSidebarWidth
        self.openSidebarWidth = openSidebarWidth

        # # content in sidebar
        # self.content = Window(self.screen, x, y, z, self.closedSidebarWidth, height)
        # self.content.addObject(Text(screen, 0, 0, 0, self.openSidebarWidth, 50, "MATH", (255, 0, 0)))
        # self.content.addObject(TextBox(screen, 0, 50, 0, 200, 50))

        # # add content
        # self.addObject(self.content)

        # quickbar
        self.quickbar = Window(self.screen, 0, 0, 0, self.closedSidebarWidth, height)
        self.quickbarRect = Rect(screen, 0, 0, 0, self.closedSidebarWidth, height, Color.BLUE1)

        self.quickbar.addObject(self.quickbarRect)

        # current Window
        self.mainNavigation = Window(self.screen, self.closedSidebarWidth, 0, 0, 0, height)
        self.mainNavigationRect = Rect(screen, 0, 0, 0, self.openSidebarWidth - self.closedSidebarWidth, height, Color.BLUE2)
        self.mainNavigationRect.br_tr = 20
        self.mainNavigationRect.br_br = 20

        self.mainNavigation.addObject(self.mainNavigationRect)
        self.mainNavigation.addObject(Text(screen, 0, 10, 0, self.openSidebarWidth - self.closedSidebarWidth, 40, "Navigation", Color.WHITE))

        # add content
        self.addObject(self.quickbar)
        self.addObject(self.mainNavigation)

        # inital close of sidebar
        self.close()

        # animation
        self.animationSpeed = 2

    def close(self):
        self.sidebarOpen = False

        self.quickbarRect.changeBorderRadius(20)
        # self.mainNavigation.hide()

    def open(self):
        self.sidebarOpen = True
        # self.mainNavigation.show()

        self.quickbarRect.changeBorderRadius(0)
        self.quickbarRect.br_tl = 20
        self.quickbarRect.br_bl = 20

    def mouseEnter(self, args: MouseEventArgs):
        self.open()

    def mouseLeave(self, args: MouseEventArgs):
        self.close()

    def update(self, dt):
        if self.sidebarOpen:
            if self.width < self.openSidebarWidth:
                self.width += self.animationSpeed * dt

                if self.width > self.openSidebarWidth:
                    self.width = self.openSidebarWidth

                self.mainNavigation.width = self.width - self.closedSidebarWidth
                self.calcRealPosition()
        else:
            self.width = self.closedSidebarWidth
            self.mainNavigation.width = 0

            self.calcRealPosition()

    def render(self):
        if self.sidebarOpen:
            self.mainNavigation.render()

        self.quickbar.render()
            
        # pygame.draw.rect(self.screen, (255, 0, 0), rect=pygame.Rect(self.realX, self.realX, self.realWidth, self.realHeight), width = 1)