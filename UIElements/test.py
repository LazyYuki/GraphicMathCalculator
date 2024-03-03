from WindowOverlayHelper.WindowObject import WindowObject
from EventManager.EventArgs import MouseEventArgs

class Test(WindowObject):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int) -> None:
        super().__init__(screen, x, y, z, width, height)

    def mouseOnClick(self, eventArgs: MouseEventArgs):
        pass