import pygame
from typing import Self

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

    def __init__(self: Self, settings: ApplicationSettings) -> None:
        self.settings = settings

    def _preLaunch(self: Self) -> bool:
        pygame.init()

        self._screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        pygame.display.set_caption(f"{self.settings.title} | 0.1.0-beta")

        self._clock = pygame.time.Clock()

        return True

    def _executionLoop(self: Self) -> bool:
        while True:
            deltaTime = self._clock.tick(self.settings.targetFps)

            # TODO: more differentation between each component: InputComponent, UpdateComponent, RenderComponent, etc.
            # -- Input Component --
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        return True

            # -- Update Component --
            ...

            # -- Render Component --
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
