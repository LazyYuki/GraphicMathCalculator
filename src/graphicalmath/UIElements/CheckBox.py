import pygame, copy

from WindowOverlayHelper.Window import Window
from UIElements.Text import Text
from UIElements.Rect import Rect
from application.color import Color
from EventManager.EventArgs import MouseEventArgs, KeyboardEventArgs

class CheckBox(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int, 
                 colorClicked = Color.BLUE1, colorEmpty = Color.WHITE, hoverColor = Color.GRAY1,
                 onClick = None, onClickArg = None) -> None:
        super().__init__(screen, x, y, z, width, height)

        self.border = Rect(screen, 0, 0, 0, width, height, color=colorEmpty, borderRadius=10)
        self.border.borderWidth = 3
        self.filled = Rect(screen, 0, 0, 0, width, height, color=colorEmpty, borderRadius=10)
        self.filled.absoluteHide()

        self.addObject(self.filled)
        self.addObject(self.border)

        self.hovered = False
        self.clicked = False

        self.onClick = onClick
        self.onClickArg = onClickArg

        self.colorClicked = colorClicked
        self.colorEmpty = colorEmpty
        self.hoverColor = hoverColor

        self.value = False

    def mouseEnter(self, args):
        self.hovered = True
        if not self.value:
            self.filled.absoluteShow()
            self.filled.color = self.hoverColor
    
    def mouseLeave(self, args):
        self.hovered = False
        if not self.value:
            self.filled.absoluteHide()

    def mouseOnClick(self, args):
        self.value = not self.value

        if self.value == True:
            self.filled.color = self.colorClicked
            self.filled.absoluteShow()

        elif self.hovered:
            self.filled.color = self.hoverColor
            self.filled.absoluteShow()

        else:
            self.filled.absoluteHide()

        if self.onClick != None:
            self.onClick(self, self.onClickArg, args)

    def render(self):
        super().render()