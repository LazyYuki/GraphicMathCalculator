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
        self.forceHoverShow = False

        self.boxColor = (0, 0, 0)
        self.clickColor = (255, 0, 0)
        self.forceClickedShow = False

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
    basic.clickColor = Color.PERSIANBLUE
    basic.text = ""
    basic.center = True
    basic.fontSize = 21
    basic.textColor = Color.WHITE
    basic.borderRadius = 15
    basic.noFill = True
    basic.borderWidth = 5

    matrix = TextBoxStyle()
    matrix.noRect = True
    matrix.forceHoverShow = True
    matrix.forceClickedShow = True
    matrix.clickColor = Color.DARK1
    matrix.borderRadius = 15
    matrix.text = ""
    matrix.fontSize = 20

class TextBox(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int, standardText = "", text = "", textBoxStyle = TextBoxStyles.basic) -> None:
        super().__init__(screen, x, y, z, width, height)

        self.changeStyle(textBoxStyle)
        self.standardText = standardText

        if text == "":
            self.text.setText(self.standardText)
        else:
            self.text.setText(text)

        self.clicked = False
        self.cursor = 0
        self.hoverd = False

        self.onChangeText = None
        self.onChangeTextArgs = None

        self.onEnter = None
        self.onEnterArgs = None

    def changeStyle(self, textBoxStyle: TextBoxStyle, text = None):
        self.textBoxStyle = copy.deepcopy(textBoxStyle)

        self.styleRect = Rect(self.screen, 0, 0, 0, self.width, self.height, self.textBoxStyle.boxColor, self.textBoxStyle.borderRadius)
        if self.textBoxStyle.noFill:
            self.styleRect.borderWidth = self.textBoxStyle.borderWidth
        self.addObject(self.styleRect)

        if text != None:
            self.textBoxStyle.text = text

        self.text = Text(self.screen, self.textBoxStyle.borderWidth, self.textBoxStyle.borderWidth, 0, 
                         self.width - self.textBoxStyle.borderWidth - 2, self.height - self.textBoxStyle.borderWidth - 2, 
                         self.textBoxStyle.text, self.textBoxStyle.textColor, self.textBoxStyle.fontPath, self.textBoxStyle.fontSize)
        self.text.center = self.textBoxStyle.center
        self.text.verticalCenter = self.textBoxStyle.verticalCenter
        
        self.addObject(self.text)

    def mouseEnter(self, args: MouseEventArgs):
        self.hoverd = True
        if not self.clicked:
            self.styleRect.color = self.textBoxStyle.hoverColor

    def mouseLeave(self, args: MouseEventArgs):
        self.hoverd = False
        if not self.clicked:
            self.styleRect.color = self.textBoxStyle.boxColor

    def mouseOnClick(self, args: MouseEventArgs):
        self.clicked = True 
        self.styleRect.color = self.textBoxStyle.clickColor

        if self.text.text != "" and self.cursor == 0:
            self.text.setText("")

    def keyPress(self, args: KeyboardEventArgs):
        # TODO: multiple line text box with enter + shift

        # key input doesnt matter
        if not self.clicked:
            return
        
        # enter = get out of there
        if args.isPressed(pygame.K_RETURN):
            self.enter()

            return
        
        # delete last from text
        if args.isPressed(pygame.K_BACKSPACE):
            if self.cursor != 0:
                self.cursor -= 1
                self.text.setText(self.text.text[:-1])

            return
        
        upperCase = args.isDown(pygame.K_LSHIFT) or args.isDown(pygame.K_RSHIFT) 
        
        t = self.text.text

        # add keys to this
        key: KeyEventArgs
        for key in args.pressed:
            c = key.unicode

            if c.isalpha():
                if upperCase:
                    t += c.upper()
                    continue

            t += c
            self.cursor += 1

        self.text.setText(t)

        if self.onChangeText != None:
            self.onChangeText(self.onChangeTextArgs)

    def enter(self):
        self.clicked = False

        if self.text.text == "":
            self.text.setText(self.standardText)

        self.styleRect.color = self.textBoxStyle.boxColor

        if self.onEnter != None:
            self.onEnter(self.onEnterArgs)

    def getText(self):
        return self.text.text

    def setText(self, text):
        self.text.setText(text)
        self.cursor = len(text)

    def render(self):
        if not self.textBoxStyle.noRect or (self.textBoxStyle.forceHoverShow and self.hoverd) or (self.textBoxStyle.forceClickedShow and self.clicked):
            self.styleRect.render()

        if not self.textBoxStyle.noText:
            self.text.render()