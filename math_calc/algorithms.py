from math import *

def bisektion(f, y_0: float, a: float, b: float, eps: float = 0.000001):
    while abs(a-b) >= eps:
        m = (a+b)/2
        if (f(a)-y_0) * (f(m)-y_0) < 0:
            b = m
        else: a = m
    return round(m, 2)
