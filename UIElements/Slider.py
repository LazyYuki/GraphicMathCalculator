import pygame, copy, math, types

from WindowOverlayHelper.Window import Window
from UIElements.Text import Text
from UIElements.Rect import Rect
from Application.Color import Color
from EventManager.EventArgs import MouseEventArgs, KeyboardEventArgs

def mouseDown(self, args):
    if self.down:
        return

    self.startMouseX = args.x
    self.startX = self.x
    self.down = True

def mouseOnUpAlways(self, args):
    self.down = False

def update(self, dt):
    if self.down:
        args = self.parent.eventManager.mouseEventArgs

        theoreticalX = args.x - self.startMouseX + self.startX

        sliderW = self.parent.width - self.parent.height

        if theoreticalX < 0:
            theoreticalX = 0
        elif theoreticalX > sliderW:
            theoreticalX = sliderW

        self.parent.value = theoreticalX / (sliderW) * (self.parent.maxValue - self.parent.minValue) + self.parent.minValue
        self.parent.setValue(round(self.parent.value) if self.parent.round else self.parent.value)

        self.calcRealPosition()
        

class Slider(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int, 
                 colorFilled = Color.BLUE1, colorNotFilled = Color.GRAY1, onValueChange=None, onValueChangeArgs = None) -> None:
        super().__init__(screen, x, y, z, width, height)

        if height % 2 == 0:
            height += 1

            print("WARNING: SLIDER HEIGHT MUST BE ODD (for style :D)")

        mh = height / 2
        sliderRectHeight = height / 3
        l = math.floor(sliderRectHeight / 3)
        r = math.ceil(sliderRectHeight / 3)

        self.styleRectLeft = Rect(screen,  math.ceil(mh), mh - r, 0, width - height, sliderRectHeight, color=colorFilled, borderRadius=100)
        self.styleRectRight = Rect(screen, math.ceil(mh), mh - r, 0, width - height, sliderRectHeight, color=colorNotFilled, borderRadius=100)

        self.styleCircle = Rect(screen, 0, 0, 0, height, height, color=colorFilled, borderRadius=100)
        self.styleCircle.down = False
        self.styleCircle.update = types.MethodType( update, self.styleCircle )
        self.styleCircle.mouseDown = types.MethodType( mouseDown, self.styleCircle )
        self.styleCircle.mouseOnUpAlways = types.MethodType( mouseOnUpAlways, self.styleCircle )

        self.addObject(self.styleRectRight)
        self.addObject(self.styleRectLeft)
        self.addObject(self.styleCircle)

        self.minValue = 0
        self.maxValue = 100

        self.round = True
        self.clicked = False

        self.onValueChange = onValueChange
        self.onValueChangeArgs = onValueChangeArgs

        self.value = self.minValue
        self.setValue(self.value - 1)   
        
    def setValue(self, newValue, functionCall = True):
        if self.value == newValue:
            return

        if self.value < self.minValue:
            self.value = self.minValue

        elif self.value > self.maxValue:
            self.value = self.maxValue

        else:
            self.value = newValue

        self.styleCircle.x = (self.value - self.minValue) / (self.maxValue - self.minValue) * (self.width - self.height)
        self.styleRectLeft.width = self.styleCircle.x

        if functionCall and self.onValueChange != None:
            self.onValueChange(self, self.onValueChangeArgs)

    def setMinValue(self, minValue):
        self.minValue = minValue
        self.setValue(self.minValue)

    def setMaxValue(self, maxValue):
        self.maxValue = maxValue
        self.setValue(self.minValue)       

    def getValueFromRealX(self, args):
        theoreticalX = args.x - self.realX - self.height / 2

        sliderW = self.width - self.height

        if theoreticalX < 0:
            theoreticalX = 0
        elif theoreticalX > sliderW:
            theoreticalX = sliderW

        self.value = theoreticalX / (sliderW) * (self.maxValue - self.minValue) + self.minValue

        return round(self.value) if self.round else self.value

    def getValue(self):
        return self.value

    def mouseOnClick(self, args):
        self.clicked = True
        self.clickedValue = self.getValueFromRealX(args)

    def update(self, dt: float):
        super().update(dt)

        if self.clicked:
            self.clicked = False

            if self.styleCircle.down == True:
                return
            
            self.setValue(self.clickedValue)

    def render(self):
        super().render()