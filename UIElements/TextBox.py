import pygame, copy

from WindowOverlayHelper.Window import Window
from Application.Color import Color
from EventManager.EventArgs import *
from UIElements.AllUIElements import Rect, Text

class TextBoxStyle:
    def __init__(self) -> None:
        self.fontPath = ""

        self.hoverColor = Color.DARK1
        self.hoverEnterFunction = None
        self.hoverLeaveFunction = None

        self.boxColor = (0, 0, 0)
        self.clickColor = (255, 0, 0)
        self.clickAnimation = True

        self.borderRadius = 0
        self.borderWidth = 0
        self.noRect = False
        self.noFill = False

        self.fontPath = "Assets/Fonts/Inter.ttf"
        self.fontSize = 20

        self.text = "TextBox"
        self.textColor = (255, 255, 255)
        self.noText = False
        self.center = True
        self.verticalCenter = False

        self.activeColor = Color.BLUE3

class TextBoxStyles:
    basic = TextBoxStyle()
    basic.hoverColor = Color.BLUE2
    basic.boxColor = Color.BLUE1
    basic.clickColor = Color.BLUE3
    basic.text = ""
    basic.fontSize = 16
    basic.textColor = Color.WHITE
    basic.borderRadius = 15
    basic.noFill = True
    basic.borderWidth = 5

class TextBox(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int, text = "", textBoxStyle = TextBoxStyles.basic) -> None:
        super().__init__(screen, x, y, z, width, height)

        self.changeStyle(textBoxStyle, text)

        self.textBoxClicked = False
        self.text = ""
        self.cursor = 0

        self.text = Text(screen, 0, 0, 0,)

    def changeStyle(self, textBoxStyle: TextBoxStyle, text = None):
        self.textBoxStyle = copy.deepcopy(textBoxStyle)

        self.styleRect = Rect(self.screen, 0, 0, 0, self.width, self.height, self.textBoxStyle.boxColor, self.textBoxStyle.borderRadius)
        if self.textBoxStyle.noFill:
            self.styleRect.borderWidth = self.textBoxStyle.borderWidth
        self.addObject(self.styleRect)

        if text != None:
            self.textBoxStyle.text = text

        self.text = Text(self.screen, 0, 0, 0, self.width, self.height, self.textBoxStyle.text, self.textBoxStyle.textColor, self.textBoxStyle.fontPath, self.textBoxStyle.fontSize)
        self.text.center = self.textBoxStyle.center
        self.text.verticalCenter = self.textBoxStyle.verticalCenter
        
        self.addObject(self.text)

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