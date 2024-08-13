import pygame, copy

from WindowOverlayHelper.Window import Window
from UIElements.Text import Text
from UIElements.Rect import Rect
from application.color import Color
from EventManager.EventArgs import MouseEventArgs, KeyboardEventArgs

class ButtonStyle:
    def __init__(self) -> None:
        self.hoverColor = Color.DARK1
        self.hoverEnterFunction = None
        self.hoverLeaveFunction = None

        self.buttonColor = (0, 0, 0)
        self.clickColor = (255, 0, 0)
        self.clickAnimation = True

        self.borderRadius = 0
        self.borderWidth = 0
        self.noRect = False
        self.noFill = False

        self.fontPath = "assets/fonts/Inter.ttf"
        self.fontSize = 20

        self.text = "Button"
        self.textColor = (255, 255, 255)
        self.noText = False
        self.center = True
        self.verticalCenter = False

        self.imageSize = (35, 35)

        self.activeColor = Color.BLUE3

class ButtonStyles:
    sidebarQuickbar = ButtonStyle()
    sidebarQuickbar.hoverColor = Color.BLUE3
    sidebarQuickbar.clickAnimation = False
    sidebarQuickbar.noText = True
    sidebarQuickbar.buttonColor = Color.BLUE1
    sidebarQuickbar.borderRadius = 5
    sidebarQuickbar.text = "image"

    sidebarMainNavigation = ButtonStyle()
    sidebarMainNavigation.hoverColor = Color.BLUE3
    sidebarMainNavigation.buttonColor = Color.BLUE2
    sidebarMainNavigation.clickColor = Color.BLUE2
    sidebarMainNavigation.noRect = False
    sidebarMainNavigation.noFill = True
    sidebarMainNavigation.text = "Test"
    sidebarMainNavigation.textColor = Color.WHITE
    sidebarMainNavigation.borderRadius = 15
    sidebarMainNavigation.verticalCenter = True
    sidebarMainNavigation.center = False

    basic = ButtonStyle()
    basic.hoverColor = Color.BLUE2
    basic.buttonColor = Color.BLUE1
    basic.clickColor = Color.BLUE3
    basic.text = "Click Me"
    basic.fontSize = 16
    basic.textColor = Color.WHITE
    basic.borderRadius = 15



class Button(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int, buttonStyle = ButtonStyles.basic, onClick = None, onClickArg = None, text=None) -> None:
        super().__init__(screen, x, y, z, width, height)

        self.changeStyle(buttonStyle, text)
        self.hovered = False
        self.clicked = False

        self.onClick = onClick
        self.onClickArg = onClickArg

        self.active = False

    def changeStyle(self, buttonStyle: ButtonStyle, text = None):
        self.buttonStyle = copy.deepcopy(buttonStyle)

        self.styleRect = Rect(self.screen, 0, 0, 0, self.width, self.height, self.buttonStyle.buttonColor, self.buttonStyle.borderRadius)
        if self.buttonStyle.noFill:
            self.styleRect.borderWidth = self.buttonStyle.borderWidth
        self.addObject(self.styleRect)

        if text != None:
            self.buttonStyle.text = text

        self.text = Text(self.screen, 0, 0, 0, self.width, self.height, self.buttonStyle.text, self.buttonStyle.textColor, self.buttonStyle.fontPath, self.buttonStyle.fontSize)
        self.text.center = self.buttonStyle.center
        self.text.verticalCenter = self.buttonStyle.verticalCenter
        
        self.addObject(self.text)

    def mouseEnter(self, args):
        self.hovered = True
        self.styleRect.color = self.buttonStyle.hoverColor
    
    def mouseLeave(self, args):
        self.hovered = False
        if self.active:
            self.styleRect.color = self.buttonStyle.activeColor
        else:    
            self.styleRect.color = self.buttonStyle.buttonColor

    def activate(self):
        self.styleRect.color = self.buttonStyle.activeColor
        self.active = True

    def deactivate(self):
        self.styleRect.color = self.buttonStyle.buttonColor
        self.active = False

    def mouseOnClick(self, args):
        if self.buttonStyle.clickAnimation:
            self.styleRect.color = self.buttonStyle.clickColor
        self.clicked = True

        if self.onClick != None:
            self.onClick(self, self.onClickArg, args)

    def render(self):
        if not self.buttonStyle.noRect:
            self.styleRect.render()

        if not self.buttonStyle.noText:
            self.text.render()
        
        if self.buttonStyle.clickAnimation and self.clicked:
            self.styleRect.color = self.buttonStyle.hoverColor
            self.clicked = False

class ButtonImage(Button):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int, image, buttonStyle = ButtonStyles.sidebarQuickbar, onClick = None, onClickArg = None) -> None:
        self.imagePath = image
        
        super().__init__(screen, x, y, z, width, height, buttonStyle, onClick, onClickArg)


    def changeStyle(self, buttonStyle: ButtonStyle, text=None):
        super().changeStyle(buttonStyle)

        self.image = pygame.image.load(self.imagePath)
        self.image = pygame.transform.smoothscale(self.image, self.buttonStyle.imageSize)

        self.centerCoords = (self.width // 2, self.height // 2)

    def render(self):
        super().render()

        self.screen.blit(self.image, self.image.get_rect(center = (self.centerCoords[0] + self.realX, self.centerCoords[1] + self.realY)))