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