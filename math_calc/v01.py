from math import *
from algorithms import bisektion


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

    def get_root(self, min_x: float, max_x: float, acc: float = 0.1) -> float:
        pass

    def call_y(self, x: float) -> float:
        """
        return y value for a given x value
        """
        return self(x)

    def call_x(self, y_0: float, min_x: float, max_x: float, acc: float = 0.1) -> float:
        """
        return x value for a given y value
        """
        output = [] 
        points = self.draw(min_x, max_x, acc)
        start = points[0]
        criterium = (lambda y: y < y_0) if start[1] > y_0 else (lambda y: y > y_0)
        for p in points[1:]:
            if p[1] == y_0: 
                output.append(p)
                start = p
                criterium = (lambda y: y < y_0) if start[1] > y_0 else (lambda y: y > y_0)
            elif criterium(p[1]):
                print(p)
                x = bisektion(self, y_0, start[0], p[0])
                output.append((x, y_0))
                start = p
                criterium = (lambda y: y < y_0) if start[1] > y_0 else (lambda y: y > y_0)
        return output

    
    
        

f = Function(input("f(x) = "))
print(f.call_x(4, -5, 5))
