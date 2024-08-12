import pygame

from UIElements.AllUIElements import *
from UIElements.Matrix import Matrix
from WindowOverlayHelper.Window import Window

EINFUEHRUNGS_TEXT = "Das Ziel dieser Anwendung ist es, eine einfache und intuitive Möglichkeit zu bieten, Mathematik der Oberstufe zu verstehen. Bei Fragen und Fehlern bitte an uns Wenden.\n~ Fynn, Damian, Arwed"
EINFUEHRUNGS_TIPPS = "Tipp: In den einzelnen Seiten sind wichtige Informationen mit \"Tipp:\" gekennzeichnet. Teilweise kann man Scrollen. Der Status der Seite wird durch die Icons hier angezeigt."

class Home(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int):
        super().__init__(screen, x, y, z, width, height)

        # w: 1110, h: 800

        # === Main Window

        self.headline = Text(self.screen, 0, 0, 0, self.width, 100, "Home", fontSize=70, fontPath="Assets/Fonts/HEADLINE.ttf")
        self.headline.center = True
        self.addObject(self.headline)

        self.subWindow = Window(self.screen, 10, 110, 0, self.width - 20, self.height - 130)
        self.addObject(self.subWindow)

        self.margin = 20
        sizeW = self.subWindow.width / 2
        sizeH = self.subWindow.height / 2

        w1 = Window(self.screen, 0, 0, 0, sizeW - self.margin, sizeH - self.margin)
        w1.addObject(Rect(self.screen, 0, 0, 0, w1.width, w1.height, color=Color.BLUE1, borderRadius=30, borderWidth=5))

        w1t1 = Text(self.screen, 0, 0, 0, w1.width, 50, "Einführung", fontSize=30, fontPath="Assets/Fonts/Inter.ttf")
        w1t1.center = True
        w1t1.font.bold = True
        w1.addObject(w1t1)

        w1t2 = MultiLineText(self.screen, 10, 60, 0, w1.width - 20, w1.height - 70, EINFUEHRUNGS_TEXT, fontSize=17)
        w1t3 = MultiLineText(self.screen, 10, w1t2.height + w1t2.y + 10, 0, w1.width - 20, w1.height - 70, EINFUEHRUNGS_TIPPS, fontSize=15)
        w1.addObject(w1t2)
        w1.addObject(w1t3)

        w1.addObject(Image(self.screen, 20 + w1.width / 3 * 0,  w1t3.height + w1t3.y + 20, 0, 25, 25, "Assets/Images/Check.png"))
        w1.addObject(Text(self.screen,  50 + w1.width / 3 * 0,  w1t3.height + w1t3.y + 20, 0, 100, 25, "- Fertig", fontSize=17, verticalCenter=True))
        
        w1.addObject(Image(self.screen, 25 + w1.width / 4 * 1,  w1t3.height + w1t3.y + 20, 0, 25, 25, "Assets/Images/Cross.png"))
        w1.addObject(Text(self.screen,  55 + w1.width / 4 * 1,  w1t3.height + w1t3.y + 20, 0, 200, 25, "- Nicht funktional", fontSize=17, verticalCenter=True))

        w1.addObject(Image(self.screen, 20 + w1.width / 3 * 2,  w1t3.height + w1t3.y + 20, 0, 25, 25, "Assets/Images/Exclamation.png"))
        w1.addObject(Text(self.screen,  50 + w1.width / 3 * 2,  w1t3.height + w1t3.y + 20, 0, 100, 25, "- In Arbeit", fontSize=17, verticalCenter=True))

        # == w2 - Algebra ==

        w2 = Window(self.screen, sizeW + self.margin, 0, 0, sizeW - self.margin, sizeH - self.margin)
        w2.addObject(Rect(self.screen, 0, 0, 0, w2.width, w2.height, color=Color.BLUE1, borderRadius=25, borderWidth=5))

        # == w3 - Analysis ==

        w3 = Window(self.screen, 0, sizeH + self.margin, 0, sizeW - self.margin, sizeH - self.margin)
        w3.addObject(Rect(self.screen, 0, 0, 0, w3.width, w3.height, color=Color.BLUE1, borderRadius=25, borderWidth=5))

        # == w4 - Stochastik ==

        w4 = Window(self.screen, sizeW + self.margin, sizeH + self.margin, 0, sizeW - self.margin, sizeH - self.margin)
        w4.addObject(Rect(self.screen, 0, 0, 0, w4.width, w4.height, color=Color.BLUE1, borderRadius=25, borderWidth=5))

        for w in [w1, w2, w3, w4]:
            self.subWindow.addObject(w)

        

    windowSubWindowDirHeight = 40
    windowSubWindowFileHeight = 35
    windowSubWindowIndent = 20
    def windowAddDirectoryStructure(self, dirPath, subWindow: Window, level):
        if not hasattr(subWindow, 'helperVarwindow'):
            subWindow.helperVarwindow = 50

        sub = [f for f in os.scandir(dirPath)]

        indent = level * self.windowSubWindowIndent
        w = subWindow.width

        for f in sub:
            if f.is_dir() and not f.name.startswith("__"):
                subWindow.addObject(Text(self.screen, indent, subWindow.helperVarwindow, 0, w - indent, self.windowSubWindowDirHeight, f.name, fontSize=25))
                subWindow.helperVarwindow += self.windowSubWindowDirHeight + 5

                self.windowAddDirectoryStructure(f.path, subWindow, level + 1)

            elif f.is_file():
                if f.name.endswith(".py") == False: continue

                i 
                t = Text(self.screen, 0, subWindow.helperVarwindow, 0, 
                           w, self.windowSubWindowFileHeight,
                           text=f.name.replace(".py", "").replace("_", " "), 
                           fontSize=20, fontPath="Assets/Fonts/VeraMono.ttf")
                t.indent = indent

                subWindow.addObject(t)
                subWindow.helperVarwindow += self.windowSubWindowFileHeight + 5
module = Home