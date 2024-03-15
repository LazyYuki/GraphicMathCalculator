import pygame

from WindowOverlayHelper.WindowObject import WindowObject
from EventManager.EventArgs import *

class Test(WindowObject):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int) -> None:
        super().__init__(screen, x, y, z, width, height)

        self.color = (255, 255, 255)

    def render(self):
        pygame.draw.rect(self.screen, self.color, self.getRealRect())

    def mouseEnter(self, eventArgs: MouseEventArgs):
        self.color = (0, 255, 0)

    def mouseOnClick(self, eventArgs: MouseEventArgs):
        self.color = (255, 0, 0)

    def mouseLeave(self, eventArgs: MouseEventArgs):
        self.color = (255, 255, 255)

    def keyPress(self, eventArgs: KeyboardEventArgs):
        self.x -= 50

    def keyUp(self, eventArgs: KeyboardEventArgs):
        self.x += 50