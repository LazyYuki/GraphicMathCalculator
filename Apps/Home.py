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

        self.dirStruct = {}
        self.loadDirectoryStructure("Apps", self.dirStruct)

        newLines = []
        with open("Apps/Status.txt", "r", encoding="utf-8") as f:
            txtLines = f.readlines()
            newLines = self.loadStatusTxt(txtLines, self.dirStruct)[0]

        with open("Apps/Status.txt", "w", encoding="utf-8") as f:
            f.writelines(newLines)

        print(newLines)
        # print(self.dirStruct)

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

        w2t1 = Text(self.screen, 0, 0, 1, w2.width, 50, "Algebra", fontSize=30, fontPath="Assets/Fonts/Inter.ttf", center=True)
        w2t1.font.bold = True
        w2.addObject(Rect(self.screen, 0, 0, 1, w2.width, 50, Color.BLACK))
        w2.addObject(w2t1)

        w2Scroll = ScrollWindow(self.screen, 30, 60, 2, w2.width - 60, w2.height - 60)
        w2Scroll.maxScroll = 0
        w2Scroll.scrollSpeed = 10
        w2.addObject(w2Scroll)
        self.windowDirStructure(self.dirStruct["Algebra"], w2Scroll, 0)

        w2Scroll.minScroll =  min(w2Scroll.height - w2Scroll.helperVarwindow, 0)

        w2.addObject(Rect(self.screen, 0, w2.height - 2 , 1, w2.width, 25, color=Color.BLACK))
        

        # == w3 - Analysis ==

        w3 = Window(self.screen, 0, sizeH + self.margin, 0, sizeW - self.margin, sizeH - self.margin)
        w3.addObject(Rect(self.screen, 0, 0, 0, w3.width, w3.height, color=Color.BLUE1, borderRadius=25, borderWidth=5))

        w3t1 = Text(self.screen, 0, 0, 1, w3.width, 50, "Analysis", fontSize=30, fontPath="Assets/Fonts/Inter.ttf", center=True)
        w3t1.font.bold = True
        w3.addObject(Rect(self.screen, 0, 0, 1, w3.width, 50, Color.BLACK))
        w3.addObject(w3t1)

        w3Scroll = ScrollWindow(self.screen, 30, 60, 2, w3.width - 60, w3.height - 60)
        w3Scroll.maxScroll = 0
        w3Scroll.scrollSpeed = 10
        w3.addObject(w3Scroll)
        self.windowDirStructure(self.dirStruct["Analysis"], w3Scroll, 0)

        w3Scroll.minScroll =  min(w3Scroll.height - w3Scroll.helperVarwindow, 0)

        w3.addObject(Rect(self.screen, 0, w3.height - 2 , 1, w3.width, 25, color=Color.BLACK))

        # == w4 - Stochastik ==

        w4 = Window(self.screen, sizeW + self.margin, sizeH + self.margin, 0, sizeW - self.margin, sizeH - self.margin)
        w4.addObject(Rect(self.screen, 0, 0, 0, w4.width, w4.height, color=Color.BLUE1, borderRadius=25, borderWidth=5))

        w4t1 = Text(self.screen, 0, 0, 1, w4.width, 50, "Stochastik", fontSize=30, fontPath="Assets/Fonts/Inter.ttf", center=True)
        w4t1.font.bold = True
        w4.addObject(Rect(self.screen, 0, 0, 1, w4.width, 50, Color.BLACK))
        w4.addObject(w4t1)

        w4Scroll = ScrollWindow(self.screen, 30, 60, 2, w4.width - 60, w4.height - 60)
        w4Scroll.maxScroll = 0
        w4Scroll.scrollSpeed = 10
        w4.addObject(w4Scroll)
        self.windowDirStructure(self.dirStruct["Stochastik"], w4Scroll, 0)

        w4Scroll.minScroll =  min(w4Scroll.height - w4Scroll.helperVarwindow, 0)

        w4.addObject(Rect(self.screen, 0, w4.height - 2 , 1, w4.width, 25, color=Color.BLACK))

        for w in [w1, w2, w3, w4]:
            self.subWindow.addObject(w)

    def loadDirectoryStructure(self, dirPath, dir):
        if "Apps" not in dir:
            dir["Apps"] = []

        sub = [f for f in os.scandir(dirPath)]

        for f in sub:
            if f.is_dir() and not f.name.startswith("__"):
                dir[f.name] = {"Apps":[]}
                self.loadDirectoryStructure(f.path, dir[f.name])

            elif f.is_file():
                if f.name.endswith(".py") == False: continue

                dir["Apps"].append([f.name, 0])

    def loadStatusTxt(self, txtLines, dir):
        newLines = []

        index = 0
        for i in range(len(dir["Apps"])):
            name2, status2 = dir["Apps"][i]

            if i < len(txtLines):
                name1, status1 = txtLines[i].replace("\n", "").split("=")
                
                index = i + 1

                if name1 == name2:
                    status2 = int(status1)
                    dir["Apps"][i][1] = status2

            newLines.append(f"{name2}={status2}\n")

        newLines.append("\n")
        txtLines = txtLines[index+1:]

        for name, d in dir.items():
            if name == "Apps": continue

            n, t = self.loadStatusTxt(txtLines, d)
            txtLines = t
            newLines += n

        return newLines, txtLines

        
    windowSubWindowDirHeight = 25
    windowSubWindowFileHeight = 25
    windowSubWindowIndent = 20
    def windowDirStructure(self, dirStruct, subWindow: Window, level):
        if not hasattr(subWindow, 'helperVarwindow'):
            subWindow.helperVarwindow = 0

        indent = level * self.windowSubWindowIndent
        w = subWindow.width

        for name, status in dirStruct["Apps"]:
            t = Text(self.screen, 0, subWindow.helperVarwindow, 0, 
                           w, self.windowSubWindowFileHeight,
                           text=name.replace(".py", "").replace("_", " "), 
                           fontSize=17)
            t.indent = indent + self.windowSubWindowFileHeight + 3
            t.verticalCenter = True

            p = ""
            match status:
                case 0:
                    p = "Assets/Images/Cross.png"
                case 1:
                    p = "Assets/Images/Exclamation.png"
                case 2:
                    p = "Assets/Images/Check.png"

            i = Image(self.screen, indent, subWindow.helperVarwindow, 0, self.windowSubWindowFileHeight, self.windowSubWindowFileHeight, p)
            
            subWindow.addObject(i)
            subWindow.addObject(t)
            subWindow.helperVarwindow += self.windowSubWindowFileHeight + 5

        for name, d in dirStruct.items():
            if name == "Apps": continue

            subWindow.addObject(Text(self.screen, indent, subWindow.helperVarwindow, 0, w - indent, self.windowSubWindowDirHeight, name, fontSize=17, verticalCenter=True))
            subWindow.helperVarwindow += self.windowSubWindowDirHeight + 5

            self.windowDirStructure(d, subWindow, level + 1)

                
module = Home