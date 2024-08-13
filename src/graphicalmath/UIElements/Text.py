import pygame, os

from WindowOverlayHelper.WindowObject import WindowObject
from WindowOverlayHelper.Window import Window
from EventManager.EventArgs import MouseEventArgs, KeyboardEventArgs

class Text(WindowObject):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int, text="", color = (255, 255, 255), fontPath="assets\\fonts\\Inter.ttf", fontSize = 20, center = False, verticalCenter = False) -> None:
        super().__init__(screen, x, y, z, width, height)

        self.color = color
        self.text = text

        self.renderText = ""
        
        self.renderOldWidth = width

        # self.font = pygame.font.SysFont("monospace", self.height)
        # self.font = pygame.font.Font(os.getcwd() + "\\" + fontPath.replace("/", "\\"), fontSize)
        self.fontPath = fontPath
        self.fontSize = fontSize
        self.font = pygame.font.Font(os.getcwd() + "/" + fontPath.replace("\\", "/"), int(fontSize))

        self.center = center
        self.verticalCenter = verticalCenter

        self.indent = 0

        self.clampTextToWidth()

    def setSizeFactor(self, newSizeFactor) -> bool:
        if super().setSizeFactor(newSizeFactor):
            return True

        self.indent *= self.sizeFactor
        self.fontSize *= self.sizeFactor

        self.font = pygame.font.Font(os.getcwd() + "/" + self.fontPath.replace("\\", "/"), int(self.fontSize))

    def setText(self, text):
        self.text = text
        self.clampTextToWidth()

    def clampTextToWidth(self):
        s = ""

        for c in self.text:
            if self.font.size(s + c)[0] + self.indent > self.realWidth:
                break

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

class MultiLineText(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int, text = "", color = (255, 255, 255), fontPath="assets\\fonts\\Inter.ttf", fontSize = 20):
        super().__init__(screen, x, y, z, width, height)

        self.color = color
        self.textLines = []
        self.renderTextLines = []
        
        self.renderOldWidth = width

        # self.font = pygame.font.SysFont("monospace", self.height)
        # self.font = pygame.font.Font(os.getcwd() + "\\" + fontPath.replace("/", "\\"), fontSize)
        self.fontPath = fontPath
        self.fontSize = fontSize

        self.textMargin = 3

        self.center = False
        self.verticalCenter = False

        self.text = text
        self.setTextLines(text)

    def setSizeFactor(self, newSizeFactor):
        if super().setSizeFactor(newSizeFactor):
            return True

        self.textMargin *= self.sizeFactor

        self.setTextLines(self.text)

    def setTextLines(self, text: str):
        for obj in self.objects:
            self.removeObject(obj)

        self.text = text
        self.textLines = text.split("\n")
        self.textToObj()

    def textToObj(self):
        maxH = 0
        for text in self.textLines:
            while True:
                t = Text(self.screen, 0, 0, 0, self.width, self.height, text, self.color, self.fontPath, self.fontSize)

                w, h = t.font.size(text)
                maxH = max(h, maxH)

                newText = ""
                if w > self.width:
                    splitText = t.renderText.split(" ")
                    newText = " ".join(splitText[:-1])
                    x = t.renderText
                    text = text[len(x) - len(splitText[-1]):]
                else:
                    newText = t.renderText
                    text = ""

                self.addObject(Text(self.screen, 0, 0, 0, self.width, self.height, newText, self.color, self.fontPath, self.fontSize))

                if text == "":
                    break

        currentY = 0
        for obj in self.objects:
            obj.y = currentY
            obj.height = maxH

            currentY += maxH + self.textMargin

        self.height = currentY

        self.calcRealPosition()
            
    def setCenter(self, center: bool, verticalCenter = False):
        self.center = center

        text: Text
        for text in self.objects:
            text.center = center
            text.verticalCenter = verticalCenter
