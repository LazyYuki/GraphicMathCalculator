import pygame

from WindowOverlayHelper.WindowObject import WindowObject
from EventManager.EventArgs import MouseEventArgs, KeyboardEventArgs

class Rect(WindowObject):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int, color = (255, 255, 255), borderRadius = 0) -> None:
        super().__init__(screen, x, y, z, width, height)

        self.color = color
        self.borderWidth = 0
        self.changeBorderRadius(borderRadius)

    def changeBorderRadius(self, br: int):
        self.br_tr = br
        self.br_br = br
        self.br_tl = br
        self.br_bl = br

    def render(self):
        pygame.draw.rect(self.screen, self.color, self.getRealRect(), self.borderWidth, 
                         border_top_left_radius=self.br_tl, border_top_right_radius=self.br_tr, 
                         border_bottom_left_radius=self.br_bl, border_bottom_right_radius=self.br_br) 

