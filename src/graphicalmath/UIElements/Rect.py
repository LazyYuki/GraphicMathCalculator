import pygame

from WindowOverlayHelper.WindowObject import WindowObject
from EventManager.EventArgs import MouseEventArgs, KeyboardEventArgs

class Rect(WindowObject):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int, color = (255, 255, 255), borderRadius = 0, borderWidth = 0) -> None:
        super().__init__(screen, x, y, z, width, height)

        self.color = color
        self.borderWidth = borderWidth
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

class RotatableRect(WindowObject):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int, color = (255, 255, 255), borderRadius = 0, borderWidth = 0, angle=0) -> None:
        super().__init__(screen, x, y, z, width, height)

        self.color = color
        self.borderRadius = borderRadius
        self.borderWidth = borderWidth
        self.angle = angle

        self.center = None

        self.setSize(width, height)

    def setSize(self, width: int, height: int):
        self.width = width
        self.height = height

        surface = pygame.Surface((self.width, self.height)).convert_alpha()
        alpha = 0
        surface.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)

        rect = Rect(surface, 0, 0, 0, self.width, self.height, self.color, self.borderRadius, self.borderWidth)
        rect.calcRealPosition()
        rect.render()

        self.image = surface
        
        self.setAngle(self.angle)
    
    def setAngle(self, angle: int):
        self.rotateImage = pygame.transform.rotate(self.image, angle)
        
        self.angle = angle

    def render(self):
        if self.center == None:
            self.screen.blit(self.rotateImage, (self.realX, self.realY))
        else:
            self.screen.blit(self.rotateImage, self.rotateImage.get_rect(center=(self.realX + self.center[0], self.realY + self.center[1])))