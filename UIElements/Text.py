import pygame

from WindowOverlayHelper.WindowObject import WindowObject
from EventManager.EventArgs import MouseEventArgs, KeyboardEventArgs

class Text(WindowObject):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int, text="", color = (255, 255, 255)) -> None:
        super().__init__(screen, x, y, z, width, height)

        self.color = color
        self.text = text

        self.renderText = ""
        
        self.renderOldWidth = width

        # self.font = pygame.font.SysFont("monospace", self.height)
        self.font = pygame.font.Font("Assests/Fonts/Inter.ttf", self.height)

        self.clampTextToWidth()

    def clampTextToWidth(self):
        s = ""

        for c in self.text:
            if self.font.size(s + c)[0] > self.realWidth:
                break

            s += c

        self.renderText = s

    def render(self):
        if self.renderOldWidth != self.realWidth:
            self.renderOldWidth = self.realWidth
            self.clampTextToWidth()

        r = self.font.render(self.renderText, True, self.color)

        self.screen.blit(r, (self.realX, self.realY))

