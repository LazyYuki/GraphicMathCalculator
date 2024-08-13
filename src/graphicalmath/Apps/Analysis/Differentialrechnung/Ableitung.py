from UIElements.AllUIElements import *
from WindowOverlayHelper.Window import Window

import sympy

class Derivitive(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int):
        super().__init__(screen, x, y, z, width, height)

        header = Text(screen, self.realWidth/2-300/2, 0, 0, 300, 100, "Differentialrechnung - Ableitung bilden", fontSize=30)

        self.addObject(header)

        self.addObject(Text(screen, 10, 100, 0, 300, 100, "Funktion:"))
        self.func_inp = TextBox(screen, 200, 200, 0, 300, 50, "Funktion eingeben: ")
        self.submit = Button(screen, 10, 300, 0, 300, 100, text="Ableitung bilden", onClick=self.calc_derivitive)

        self.addObject(self.func_inp)
        self.addObject(self.submit)

    def calc_derivitive(self, btn, on_clickarg, args):
        func = self.func_inp.getText()
        x = sympy.symbols("x")
        derivitive = sympy.diff(func, x)
        print(derivitive)

module = Derivitive