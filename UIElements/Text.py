import pygame

from WindowOverlayHelper.WindowObject import WindowObject
from EventManager.EventArgs import MouseEventArgs, KeyboardEventArgs

class Text(WindowObject):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int, text="", color = (255, 255, 255)) -> None:
        super().__init__(screen, x, y, z, width, height)

        self.color = color
        self.text = text

        self.font = pygame.font.SysFont("monospace", self.height)

    def render(self):
        r = self.font.render(self.text, True, self.color)

        self.screen.blit(r, (self.realX, self.realY))