from math import *
        
class Function:

    def __init__(self, value: str):
        """
        Function class for Analysis

        str: value - input-function as a string
        """
        self.value = lambda x: eval(value)
        
    def __call__(self, x: float) -> float:
        """
        returns functions value at a given point
        """
        return self.value(x)

    def draw(self, min_x: float, max_x: float, acc: float = 0.1) -> list:
        """
        returns (x, y) tuple for function points in an given interval with a given distance
        """
        points = []
        x = min_x
        while True:
            if x > max_x: return points
            points.append((x, self(x)))
            x += acc

    def call_x(self, min_x: float, max_x: float, y: float) -> float:
        amount_decimal = (10**len(str(y).split(".")[0]))
        acc=1/amount_decimal
        points = []
        x = min_x
        while True:
            if x > max_x: return points
            if round(self(x), amount_decimal) == y: points.append((round(x, amount_decimal), round(self(x), amount_decimal)))
            x += acc
        

f = Function(input("f(x) = "))
while True:
    print(f.call_x(-5, 5, float(input())))

