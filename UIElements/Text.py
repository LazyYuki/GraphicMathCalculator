import pygame, os

from WindowOverlayHelper.WindowObject import WindowObject
from EventManager.EventArgs import MouseEventArgs, KeyboardEventArgs

class Text(WindowObject):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int, text="", color = (255, 255, 255), fontPath="Assets\\Fonts\\Inter.ttf", fontSize = 20) -> None:
        super().__init__(screen, x, y, z, width, height)

        self.color = color
        self.text = text

        self.renderText = ""
        
        self.renderOldWidth = width

        # self.font = pygame.font.SysFont("monospace", self.height)
        self.font = pygame.font.Font(os.getcwd() + "\\" + fontPath.replace("/", "\\"), fontSize)

        self.center = False
        self.verticalCenter = False

        self.indent = 0

        self.clampTextToWidth()

    def clampTextToWidth(self):
        s = ""

        for c in self.text:
            if self.font.size(s + c)[0] + self.indent > self.realWidth:
                s += " "
                continue

            s += c

        self.renderText = s

    def render(self):
        if self.renderOldWidth != self.realWidth:
            self.renderOldWidth = self.realWidth
            self.clampTextToWidth()

        r = self.font.render(self.renderText, True, self.color)

        if self.center:
            self.screen.blit(r, r.get_rect(center=(self.realX + self.realWidth // 2, self.realY + self.realHeight // 2)))
        elif self.verticalCenter:
            self.screen.blit(r, r.get_rect(centery=self.realY + self.realHeight // 2, x=self.realX + self.indent))
        else:
            self.screen.blit(r, (self.realX + self.indent, self.realY))

