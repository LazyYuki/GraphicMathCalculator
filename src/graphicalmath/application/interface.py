import pygame
from typing import Self

from WindowOverlayHelper.Window import Window
from UIElements.AllUIElements import *

from .settings import ApplicationSettings

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
        pygame.display.set_caption(f"{self.settings.title} | 0.1.3-beta")

        self._clock = pygame.time.Clock()

        self._mainWindow = Window(self._screen, 0, 0, 0, self.settings.width, self.settings.height)

        self.container = Window(self._screen, 90, 0, 0, self.settings.width - 90, self.settings.height)
        self.sidebar = Sidebar(self._screen, 10, 10, 0, 300, self.settings.height - 20, container=self.container)

        self._mainWindow.addObject(self.container)
        self._mainWindow.addObject(self.sidebar)

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

                    case pygame.MOUSEWHEEL:
                        self._mainWindow.eventManager.updateMouseScroll(event)

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
    