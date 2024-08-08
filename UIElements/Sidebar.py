import pygame, os, importlib

from WindowOverlayHelper.WindowObject import WindowObject
from WindowOverlayHelper.Window import Window
from UIElements.AllUIElements import Text, Rect, Button, ButtonImage, ButtonStyles
from EventManager.EventArgs import MouseEventArgs, KeyboardEventArgs
from Application.Color import *

class Sidebar(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int, 
                 closedSidebarWidth = 72, openSidebarWidth = 350, container = None) -> None:
        """
        x y width height of total sidebar
        when closed, sidebar will be shown as circle in top left corner
        """
        super().__init__(screen, x, y, z, width, height)

        self.container = container

        self.foregroundColor = Color.BLACK
        self.backgroundColor = Color.WHITE

        self.sidebarOpen = False
        self.closedSidebarWidth = closedSidebarWidth
        self.openSidebarWidth = openSidebarWidth

        # current Window
        self.mainNavigation = Window(self.screen, self.closedSidebarWidth, 0, 0, 0, height)
        self.mainNavigation.lockDraw = True

        mainNavigationWidth = self.openSidebarWidth - self.closedSidebarWidth
        self.mainNavigationRect = Rect(screen, 0, 0, 0, mainNavigationWidth, height, Color.BLUE2)
        self.mainNavigationRect.br_tr = 20
        self.mainNavigationRect.br_br = 20

        t = Text(screen, 0, 10, 0, mainNavigationWidth, 40, "Navigation", Color.WHITE, fontSize=40)
        t.center = True

        self.mainNavigation.addObject(self.mainNavigationRect)
        self.mainNavigation.addObject(t)
        self.mainNavigation.addObject(Rect(screen, 0, self.closedSidebarWidth + 25, 0, mainNavigationWidth, 2, Color.WHITE))

        self.algebraWindow = Window(screen, 5, self.closedSidebarWidth + 32, 0, mainNavigationWidth - 10, height)
        self.algebraWindow.addObject(Text(screen, 0, 0, 0, mainNavigationWidth, 40, "Algebra", fontSize=30))
        self.mainNavigaionAddDirectoryStructure("Apps/Algebra", self.algebraWindow, 1)

        self.analysisWindow = Window(screen, 5, self.closedSidebarWidth + 32, 0, mainNavigationWidth - 10, height)
        self.analysisWindow.addObject(Text(screen, 0, 0, 0, mainNavigationWidth, 40, "Analysis", fontSize=30))
        self.mainNavigaionAddDirectoryStructure("Apps/Analysis", self.analysisWindow, 1)

        self.stochastikWindow = Window(screen, 5, self.closedSidebarWidth + 32, 0, mainNavigationWidth - 10, height)
        self.stochastikWindow.addObject(Text(screen, 0, 0, 0, mainNavigationWidth, 40, "Stochastik", fontSize=30))
        self.mainNavigaionAddDirectoryStructure("Apps/Stochastik", self.stochastikWindow, 1)

        self.mainNavigation.addObject(self.algebraWindow)
        self.mainNavigation.addObject(self.analysisWindow)
        self.mainNavigation.addObject(self.stochastikWindow)

        self.algebraWindow.absoluteHide()
        self.analysisWindow.absoluteHide()
        self.stochastikWindow.absoluteHide()

        self.mainNavigationWindows = [self.algebraWindow, self.analysisWindow, self.stochastikWindow]

        # quickbar
        self.quickbar = Window(self.screen, 0, 0, 0, self.closedSidebarWidth, height)

        self.quickbarRect = Rect(screen, 0, 0, 0, self.closedSidebarWidth, height, Color.BLUE1)
        self.quickbar.addObject(self.quickbarRect)

        mainButton = ButtonImage(self.screen, 0, 0, 0, self.closedSidebarWidth, self.closedSidebarWidth, "Assets/Images/MathIcon.png", buttonStyle=ButtonStyles.sidebarQuickbar)
        mainButton.buttonStyle.noRect = True
        mainButton.buttonStyle.imageSize = (45, 45)
        mainButton.changeStyle(mainButton.buttonStyle)
        self.quickbar.addObject(mainButton)

        self.quickbar.addObject(Rect(screen, 0, self.closedSidebarWidth + 25, 0, self.closedSidebarWidth, 2, Color.WHITE))

        b1 = ButtonImage(self.screen, 0, 1 * (self.closedSidebarWidth + 10) + 50, 0, 
                                            self.closedSidebarWidth, self.closedSidebarWidth, 
                                            "Assets/Images/AlgebraIcon.png", buttonStyle=ButtonStyles.sidebarQuickbar,
                                            onClick=(lambda b, x, y: x.quickbarButtonShow(0, b1)), onClickArg=self)
        b2 = ButtonImage(self.screen, 0, 2 * (self.closedSidebarWidth + 10) + 50, 0, 
                                            self.closedSidebarWidth, self.closedSidebarWidth, 
                                            "Assets/Images/AnalysisIcon.png", buttonStyle=ButtonStyles.sidebarQuickbar,
                                            onClick=(lambda b, x, y: x.quickbarButtonShow(1, b2)), onClickArg=self)
        b3 = ButtonImage(self.screen, 0, 3 * (self.closedSidebarWidth + 10) + 50, 0, 
                                            self.closedSidebarWidth, self.closedSidebarWidth, 
                                            "Assets/Images/StochasticIcon.png", buttonStyle=ButtonStyles.sidebarQuickbar,
                                            onClick=(lambda b, x, y: x.quickbarButtonShow(2, b3)), onClickArg=self)
        
        self.quickbarButtons = [b1, b2, b3]

        for b in self.quickbarButtons:
            self.quickbar.addObject(b)

        self.quickbar.addObject(ButtonImage(self.screen, 0, height - self.closedSidebarWidth * 1.5, 0, self.closedSidebarWidth, self.closedSidebarWidth, "Assets/Images/SettingsIcon.png", buttonStyle=ButtonStyles.sidebarQuickbar))

        self.quickbarButtonShow(0, b1)

        # add content
        self.addObject(self.quickbar)
        self.addObject(self.mainNavigation)

        # inital close of sidebar
        self.close()

        # animation
        self.animationSpeed = 1

    def quickbarButtonShow(self, i, ab = None):
        for w in self.mainNavigationWindows:
            w.absoluteHide()

        self.mainNavigationWindows[i].absoluteShow()

        for b in self.quickbarButtons:
            b.deactivate()

        if ab != None:
            ab.activate()

    mainNavigationSubWindowDirHeight = 40
    mainNavigationSubWindowFileHeight = 35
    mainNavigationSubWindowIndent = 20
    def mainNavigaionAddDirectoryStructure(self, dirPath, subWindow: Window, level):
        if not hasattr(subWindow, 'helperVarMainNavigation'):
            subWindow.helperVarMainNavigation = 50

        sub = [f for f in os.scandir(dirPath)]

        indent = level * self.mainNavigationSubWindowIndent
        w = subWindow.width

        for f in sub:
            if f.is_dir():
                subWindow.addObject(Text(self.screen, indent, subWindow.helperVarMainNavigation, 0, w - indent, self.mainNavigationSubWindowDirHeight, f.name, fontSize=25))
                subWindow.helperVarMainNavigation += self.mainNavigationSubWindowDirHeight + 5

                self.mainNavigaionAddDirectoryStructure(f.path, subWindow, level + 1)

            elif f.is_file():
                if f.name.endswith(".py") == False: continue

                b = Button(self.screen, 0, subWindow.helperVarMainNavigation, 0, 
                           w, self.mainNavigationSubWindowFileHeight, 
                           buttonStyle=ButtonStyles.sidebarMainNavigation, onClick=(lambda b, x, y: [x.close()]), onClickArg=self, text=f.name.replace(".py", "").replace("_", " "))
                b.text.indent = indent

                subWindow.addObject(b)
                subWindow.helperVarMainNavigation += self.mainNavigationSubWindowFileHeight + 5

    def loadSubWindow(self, path: str):
        if self.container == None:
            return
        
        self.container: Window

        w: Window
        for w in self.container.objects:
            w.absoluteHide()

        activeWindow = self.container.idCheck(path)
        if activeWindow != None:
            activeWindow.absoluteShow()
        else:
            mod = importlib.import_module(path.replace("/", ".").replace("\\", ".").replace(".py", ""))
            
            if hasattr(mod, "module") and mod.module != None:
                self.container.addObject(mod.module(self.screen, 0, 0, 0, self.container.width, self.container.height))
                mod.module.absoluteShow()

    def setMainNavigationPanel(self, panel: Window):
        self.mainNavigation.addObject(panel)

    def close(self):
        self.sidebarOpen = False

        self.mainNavigation.hide()

    def open(self):
        self.sidebarOpen = True
        self.mainNavigation.show()

        self.quickbarRect.changeBorderRadius(0)
        self.quickbarRect.br_tl = 20
        self.quickbarRect.br_bl = 20

    def mouseEnter(self, args: MouseEventArgs):
        self.open()

    def mouseLeave(self, args: MouseEventArgs):
        self.close()

    def update(self, dt):
        if self.sidebarOpen:
            if self.width < self.openSidebarWidth:
                self.width += self.animationSpeed * dt

                if self.width > self.openSidebarWidth:
                    self.width = self.openSidebarWidth

                self.mainNavigation.width = self.width - self.closedSidebarWidth
                self.calcRealPosition()
        else:
            if self.width > self.closedSidebarWidth:
                self.width -= self.animationSpeed * dt

                if self.width <= self.closedSidebarWidth:
                    self.width = self.closedSidebarWidth
                    self.quickbarRect.changeBorderRadius(20)

                self.mainNavigation.width = self.width - self.closedSidebarWidth

                self.calcRealPosition()

    def render(self):
        self.mainNavigation.render()

        self.quickbar.render()
            
        # pygame.draw.rect(self.screen, (255, 0, 0), rect=pygame.Rect(self.realX, self.realX, self.realWidth, self.realHeight), width = 1)