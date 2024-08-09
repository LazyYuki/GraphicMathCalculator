from UIElements.AllUIElements import *
from WindowOverlayHelper.Window import Window

class Derivitive(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int):
        super().__init__(screen, x, y, z, width, height)

        header = Text(screen, self.realWidth/2, 0, 0, 300, 100, "Differentialrechnung - Ableitung bilden", fontSize=30)

        self.addObject(header)

    def derive(self, eq: str):
        return

module = Derivitive