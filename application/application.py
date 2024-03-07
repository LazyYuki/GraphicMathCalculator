import pygame
from typing import Self

# shit imports :skull:
from WindowOverlayHelper.Window import Window
from UIElements.test import Test


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

        self.subWindow = Window(self._screen, 100, 100, 0, 100, 100)

        self.test = Test(self._screen, 50, 50, 0, 100, 100)

        self.subWindow.addObject(self.test)
        self._mainWindow.addObject(self.subWindow)

        print(self._mainWindow.eventManager.allEvents)
        print(self._mainWindow.eventManager.subManagerObjects)

        return True

    def _executionLoop(self: Self) -> bool:
        while True:
            deltaTime = self._clock.tick(self.settings.targetFps)

            # TODO: more differentation between each component: InputComponent, UpdateComponent, RenderComponent, etc.
            # -- Input Component --
            events = pygame.event.get()
            for event in events:
                match event.type:
                    case pygame.QUIT:
                        return True

            # TODO == debug code von arwed (shit) ==
            self._mainWindow.eventManager.updateEventArgs(deltaTime, events, pygame.mouse)
            self._mainWindow.eventManager.updateCurrentTriggerEvents()

            # if len(self._mainWindow.eventManager.triggerEvents):
            #     print(self._mainWindow.eventManager.triggerEvents)

            # -- Update Component --
            self._mainWindow.eventManager.triggerRegisterdEvents()

            # -- Render Component --
            self.test.render()

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
