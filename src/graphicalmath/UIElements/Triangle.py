import pygame, math

from WindowOverlayHelper.WindowObject import WindowObject
from EventManager.EventArgs import MouseEventArgs, KeyboardEventArgs

def find_circle(points):
    a, b, c = points

    midAB = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    midAC = ((a[0] + c[0]) / 2, (a[1] + c[1]) / 2)

    slopeAB = - 1 / ((b[1] - a[1]) / (b[0] - a[0]))
    slopeAC = -1 / ((c[1] - a[1]) / (c[0] - a[0]))

    nAB = midAB[1] - slopeAB * midAB[0]
    nAC = midAC[1] - slopeAC * midAC[0]

    centerX = (nAC - nAB) / (slopeAB - slopeAC)
    centerY = slopeAB * centerX + nAB

    radius = math.sqrt((centerX - a[0]) ** 2 + (centerY - a[1]) ** 2)

    return (centerX, centerY), radius

class Triangle(WindowObject):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int, tC: int, tH: int, rotation: int, lineWidth = 0, color = (255, 255, 255)) -> None:
        super().__init__(screen, x, y, z, width, height)

        self.normalPoints = [
            (tC / 2, 0),
            (0, tH),
            (tC, tH)
        ]

        self.m, self.r = find_circle(self.normalPoints)

        self.normalAngles = [math.atan2(self.m[0] - point[0], self.m[1] - point[1]) for point in self.normalPoints]

        self.rotatedPoints = []
        self.changeAngle(rotation)

        self.color = color
        self.lineWidth = lineWidth

    def changeAngle(self, angle: int):
        self.rotatedPoints = []

        rd = math.radians(angle)

        for a in self.normalAngles:
            self.rotatedPoints.append((
                self.r * math.cos(a + rd) + self.m[0],
                self.r * -math.sin(a + rd) + self.m[1]
            ))

        self.angle = angle

    def render(self):
        pygame.draw.polygon(self.screen, self.color, [(p[0] + self.realX, p[1] + self.realY) for p in self.rotatedPoints], self.lineWidth)
