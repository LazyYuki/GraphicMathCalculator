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
        self.font = pygame.font.Font(os.getcwd() + "/" + fontPath.replace("\\", "/"), fontSize)

        self.center = center
        self.verticalCenter = verticalCenter

        self.indent = 0

        self.clampTextToWidth()

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

        self.setTextLines(text)

    def setTextLines(self, text: str):
        for obj in self.objects:
            self.removeObject(obj)

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

class LetterRenderer(WindowObject):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int, fontPath="assets\\fonts\\Inter.ttf", fontSize = 20) -> None:
        super().__init__(screen, x, y, z, width, height)

        self.letters = []

        self.font = pygame.font.Font(os.getcwd() + "/" + fontPath.replace("\\", "/"), fontSize)

        self.setText([])

    def setText(self, lettersWColor: list):
        self.letters = lettersWColor
        s = ""
        self.maxH = 0

        for i in range(len(self.letters)):
            if self.letters[i][0].endswith("\n"):
                self.letters[i][0] = self.letters[i][0][:-1]
                
                if i + 1 < len(self.letters):
                    self.letters[i + 1][0] = "\n" + self.letters[i + 1][0]

            endLine = False
            if self.letters[i][0].startswith("\n"):
                self.letters[i][0] = self.letters[i][0][1:]
                endLine = True

            s += self.letters[i][0]

            self.letters[i].append(self.font.render(self.letters[i][0], True, self.letters[i][1]))
            self.letters[i].append(self.font.size(self.letters[i][0])[0])

            size = self.font.size(s)
            if size[0] > self.realWidth or endLine:
                self.letters[i][0] = "\n" + self.letters[i][0]

                if size[1] > self.maxH:
                    self.maxH = size[1]

                s = ""

    def render(self):
        x = 0
        y = 0

        for i in range(len(self.letters)):
            if self.letters[i][0].startswith("\n"):
                y += 1
                x = 0

            self.screen.blit(self.letters[i][2], (self.realX + x, self.realY + y * self.maxH))
            x += self.letters[i][3]