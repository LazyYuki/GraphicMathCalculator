import pygame, copy

from WindowOverlayHelper.Window import Window
from EventManager.EventArgs import MouseEventArgs, KeyboardEventArgs

class ScrollWindow(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int):
        super().__init__(screen, x, y, z, width, height)

        self.scrollSpeed = 5
        self.currentScroll = 0

        self.minScroll = 0
        self.maxScroll = 100

    def mouseScrollUp(self, args: MouseEventArgs):
        if self.currentScroll - self.scrollSpeed < self.minScroll:            
            for obj in self.objects:
                obj.y -= self.currentScroll

            self.currentScroll = self.minScroll

        else:
            self.currentScroll -= self.scrollSpeed

            for obj in self.objects:
                obj.y -= self.scrollSpeed

    def mouseScrollDown(self, args: MouseEventArgs):
        if self.currentScroll + self.scrollSpeed > self.maxScroll:
            for obj in self.objects:
                obj.y += self.maxScroll - self.currentScroll

            self.currentScroll = self.maxScroll

        else:
            self.currentScroll += self.scrollSpeed

            for obj in self.objects:
                obj.y += self.scrollSpeed
