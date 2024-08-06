import pygame
from typing import Self

# shit imports :skull:
from WindowOverlayHelper.Window import Window
from UIElements.test import Test
from UIElements.TextBox import TextBox
from UIElements.Sidebar import Sidebar

class ApplicationSettings:

    title: str
    width: int
    height: int
    targetFps: int

    def __init__(self: Self, title: str, width: int, height: int, targetFps: int) -> None:
        self.title = title
        self.width = width
        self.height = height
        self.targetFps = targetFps

class Application:

    settings: ApplicationSettings
    _clock: pygame.time.Clock
    _screen: pygame.Surface

    _mainWindow: Window

    def __init__(self: Self, settings: ApplicationSettings) -> None:
        self.settings = settings

    def _preLaunch(self: Self) -> bool:
        pygame.init()

        self._screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        pygame.display.set_caption(f"{self.settings.title} | 0.1.0-beta")

        self._clock = pygame.time.Clock()

        # == debug shit von arwed ==
        self._mainWindow = Window(self._screen, 0, 0, 0, self.settings.width, self.settings.height)

        self.sidebar = Sidebar(self._screen, 10, 10, 0, 300, self.settings.height - 20)

        self.subWindow = Window(self._screen, 100, 100, 1, 100, 100)

        self.textBox = TextBox(self._screen, 250, 50, 1, 200, 40)
        self.t = TextBox(self._screen, 250, 250, 1, 200, 40)

        self._mainWindow.addObject(self.subWindow)
        self._mainWindow.addObject(self.textBox)
        self._mainWindow.addObject(self.t)
        self._mainWindow.addObject(self.sidebar)

        #print(self._mainWindow.eventManager.allEvents)
        #print(self._mainWindow.eventManager.subManagerObjects)

        self.subWindow.onlyEventItemInForeground = False

        return True

    def _executionLoop(self: Self) -> bool:
        while True:
            deltaTime = self._clock.tick(self.settings.targetFps)

            # TODO: more differentation between each component: InputComponent, UpdateComponent, RenderComponent, etc.
            # -- Input Component --

            self._mainWindow.eventManager.clearKeyboardEventArgs()
            events = pygame.event.get()
            for event in events:
                match event.type:
                    case pygame.QUIT:
                        return True
                    
                    case pygame.KEYDOWN:
                        self._mainWindow.eventManager.updateKeyboardEventArgsDOWN(event)

                    case pygame.KEYUP:
                        self._mainWindow.eventManager.updateKeyboardEventArgsUP(event)

            self._mainWindow.eventManager.updateKeyboardEventArgsDt(deltaTime)
            self._mainWindow.eventManager.updateMouseEventArgs(deltaTime, pygame.mouse)

            # TODO == debug code von arwed (shit) ==
            self._screen.fill((0,0,0))

            #self._mainWindow.eventManager.updateEventArgs(deltaTime, events, pygame.mouse, pygame.key.get_pressed())
            
            self._mainWindow.eventManager.updateCurrentTriggerEvents()

            # if len(self._mainWindow.eventManager.triggerEvents):
            #     print(self._mainWindow.eventManager.triggerEvents)

            # -- Update Component --
            self._mainWindow.eventManager.triggerRegisterdEvents()
            self._mainWindow.calcRealPosition()
            self._mainWindow.update(deltaTime)
            

            # -- Render Component --
            self._mainWindow.render()

            pygame.display.flip()

        return True

    def _destroy(self: Self):
        pygame.quit()

    def launch(self: Self) -> bool:
        if not self._preLaunch():
            return False

        status = self._executionLoop()
        self._destroy()
        return status
