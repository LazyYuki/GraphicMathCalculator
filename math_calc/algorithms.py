from math import *

def bisektion(f, y_0: float, a: float, b: float, eps: float = 0.0001):
    while abs(a-b) >= eps:
        m = (a+b)/2
        if f(a) * f(m) < y_0:
            b = m
        else: a = m
    return round(m, len(str(eps).split(".")[1]))
