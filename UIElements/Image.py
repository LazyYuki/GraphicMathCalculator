import pygame, copy

from WindowOverlayHelper.WindowObject import WindowObject
from UIElements.Text import Text
from UIElements.Rect import Rect
from Application.Color import Color
from EventManager.EventArgs import MouseEventArgs, KeyboardEventArgs

class Image(WindowObject):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int, image) -> None:
        self.imagePath = image
        
        super().__init__(screen, x, y, z, width, height)

        self.image = pygame.image.load(self.imagePath)
        self.image = pygame.transform.scale(self.image, (width, height))

        self.centerCoords = (self.width // 2, self.height // 2)
        self.center = False

    def render(self):
        if self.center:
            self.screen.blit(self.image, self.image.get_rect(center = (self.centerCoords[0] + self.realX, self.centerCoords[1] + self.realY)))
        else:
            self.screen.blit(self.image, (self.realX, self.realY))