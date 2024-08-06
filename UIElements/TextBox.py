import pygame

from WindowOverlayHelper.WindowObject import WindowObject
from EventManager.EventArgs import *

class TextBox(WindowObject):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int) -> None:
        super().__init__(screen, x, y, z, width, height)

        self.color = (0, 0, 255)

        self.textBoxClicked = False
        self.text = ""
        self.cursor = 0

        self.font = pygame.font.SysFont("monospace", self.height - 2) # -2 for width of window

    def mouseOnClick(self, args: MouseEventArgs):
        self.textBoxClicked = True 

    def keyPress(self, args: KeyboardEventArgs):
        # TODO: multiple line text box with enter + shift

        # key input doesnt matter
        if not self.textBoxClicked:
            return
        
        # enter = get out of there
        if args.isPressed(pygame.K_RETURN):
            self.textBoxClicked = False
            return
        
        # delete last from text
        if args.isPressed(pygame.K_BACKSPACE):
            if self.cursor != 0:
                self.cursor -= 1
                self.text = self.text[:-1]

            return
        
        upperCase = args.isDown(pygame.K_LSHIFT) or args.isDown(pygame.K_RSHIFT) 
        
        # add keys to this
        key: KeyEventArgs
        for key in args.pressed:
            c = key.unicode

            if c.isalpha():
                if upperCase:
                    self.text += c.upper()
                    continue

            self.text += c
            self.cursor += 1

    def render(self):
        if self.textBoxClicked:
            self.color = (0, 255, 255)
        else:
            self.color = (0, 0, 255)

        r = self.font.render(self.text, True, (255, 255, 255))
        rect = r.get_rect()

        self.screen.blit(r, (self.realX, self.realY))
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.realX, self.realY, self.realWidth, self.realHeight), 1)