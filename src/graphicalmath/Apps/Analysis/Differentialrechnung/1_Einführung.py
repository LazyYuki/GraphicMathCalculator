from UIElements.AllUIElements import *
from WindowOverlayHelper.Window import Window

import sympy

class Introduction(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int):
        super().__init__(screen, x, y, z, width, height)

        header = Text(screen, self.realWidth/2-300/2, 0, 0, 300, 100, "Einführunf in die Differentialrechnung", fontSize=30)

        self.addObject(header)

        self.addObject(Text(screen, 10, 100, 0, 300, 100, "Funktion und Intervall:"))
        self.func_inp = TextBox(screen, 200, 100, 0, 300, 50, "Funktion eingeben: ")
        self.interval = TextBox(screen, 200, 100, 0, 300, 50, "Intrevall: ")
        self.submit = Button(screen, 10, 300, 0, 300, 100, text="Bestätigen", onClick=self.draw)

        self.addObject(self.func_inp)
        self.addObject(self.submit)

    def draw(self, btn, on_clickarg, args):
        func = self.func_inp.getText()


        # x = sympy.symbols("x")
        # derivitive = sympy.diff(func, x)
        # print(derivitive)

module = Introduction