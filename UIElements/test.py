import pygame

from WindowOverlayHelper.WindowObject import WindowObject
from EventManager.EventArgs import MouseEventArgs

class Test(WindowObject):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int) -> None:
        super().__init__(screen, x, y, z, width, height)

        self.color = (255, 255, 255)

    def render(self):
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.realX, self.realY, self.width, self.height))

    def mouseOnClick(self, eventArgs: MouseEventArgs):
        self.color = (255, 0, 0)

    def mouseOnUp(self, eventArgs: MouseEventArgs):
        self.color = (255, 255, 255)