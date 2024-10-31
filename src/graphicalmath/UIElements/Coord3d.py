import pygame

from WindowOverlayHelper.Window import Window
from EventManager.EventArgs import MouseEventArgs, KeyboardEventArgs
from UIElements.AllUIElements import *

from math_calc.Vector import Vector3d

from multiprocessing.pool import ThreadPool
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.backends.backend_agg as agg

def renderMatplotLibAsync(vectors, angle, id):
    soa = np.array(vectors)

    X, Y, Z, U, V, W = zip(*soa)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.quiver(X, Y, Z, U, V, W)
    ax.set_xlim([min([0] + list(X) + list(U)), max([6] + list(X) + list(U))])
    ax.set_ylim([min([0] + list(Y) + list(V)), max([6] + list(Y) + list(V))])
    ax.set_zlim([min([0] + list(Z) + list(W)), max([6] + list(Z) + list(W))])

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    if angle is not None:
        ax.view_init(angle[0], angle[1], angle[2])

    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()

    surf = pygame.image.fromstring(raw_data, canvas.get_width_height(), "RGB")

    return surf, id

class Coord3d(Window):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int) -> None:
        super().__init__(screen, x, y, z, width, height)

        self.vectors = []

        # render pool
        self.pool = ThreadPool(processes=4)
        self.surf = {
            "0": None,
            "1": None,
            "2": None,
            "3": None
        }
        self.asyncResultList = []

        # image
        self.margin = 30

        self.renderMatplotLib()

        # checkboxes
        self.mode = [False, False, False]

        self.addObject(Text(self.screen, 610, 0, 0, 150, 40, "Ansicht:", fontSize=25, verticalCenter=True))
        checkboxwindow = Window(screen, 620, 50, 0, self.width - 620, self.height)
        self.addObject(checkboxwindow)

        checkboxwindow.addObject(Text(self.screen,      0,      0, 0, 150, 30, "YZ - Ebene:", fontSize=20, verticalCenter=True))
        self.c1 = CheckBox(self.screen,  150,    0, 0, 25, 25, onClick=lambda a, b, c: [self.resetCheckBoxes(a), self.mode.__setitem__(0, a.value)])
        checkboxwindow.addObject(Text(self.screen,      0,      30, 0, 150, 30, "XY - Ebene:", fontSize=20, verticalCenter=True))
        self.c2 = CheckBox(self.screen,  150,    30, 0, 25, 25, onClick=lambda a, b, c: [self.resetCheckBoxes(a), self.mode.__setitem__(1, a.value)])
        checkboxwindow.addObject(Text(self.screen,      0,      60, 0, 150, 30, "XZ - Ebene:", fontSize=20, verticalCenter=True))
        self.c3 = CheckBox(self.screen,  150,    60, 0, 25, 25, onClick=lambda a, b, c: [self.resetCheckBoxes(a), self.mode.__setitem__(2, a.value)])

        for _ in [self.c1, self.c2, self.c3]:
            checkboxwindow.addObject(_)

    def resetCheckBoxes(self, exceptSelf):
        self.mode = [False, False, False]

        for _ in [self.c1, self.c2, self.c3]:
            if _ is exceptSelf:
                continue

            _.setValue(False)

    def addVector(self, vector: Vector3d):
        self.vectors.append(vector)

    def removeVector(self, vector: Vector3d):
        self.vectors.remove(vector)

    def renderMatplotLib(self):
        self.surf = {
            "0": None,
            "1": None,
            "2": None,
            "3": None
        }
        self.asyncResultList = []

        self.vectorList = tuple([v.nullVectorList() for v in self.vectors])
        self.asyncResultList.append(self.pool.apply_async(renderMatplotLibAsync, args=((self.vectorList, None, "0"))))
        self.asyncResultList.append(self.pool.apply_async(renderMatplotLibAsync, args=((self.vectorList, (0, 0, 0), "1"))))
        self.asyncResultList.append(self.pool.apply_async(renderMatplotLibAsync, args=((self.vectorList, (90, -90, 0), "2"))))
        self.asyncResultList.append(self.pool.apply_async(renderMatplotLibAsync, args=((self.vectorList, (0, -90, 0), "3"))))

    def editSurf(self, surf: pygame.surface.Surface):
        size = surf.get_size()

        newW, newH = size[0] - self.margin * 2, size[1] - self.margin * 2
        cropped_region = (self.margin, self.margin, newW, newH)
        cropped_subsurf = surf.subsurface(cropped_region)

        percent = self.height / newH
        realW = newW * percent

        return cropped_subsurf
        # return pygame.transform.scale(cropped_subsurf, (int(realW), self.height))

    def update(self, dt):
        super().update(dt)

        for asyncResult in self.asyncResultList:
            if asyncResult.ready():
                surf, id = asyncResult.get()
                self.surf[id] = self.editSurf(surf)

    def render(self):
        super().render()

        if sum(self.mode) == 0:
            if self.surf["0"] is not None:
                self.screen.blit(self.surf["0"], (self.realX, self.realY))
        else:
            index = str(self.mode.index(True) + 1)

            if self.surf[index] is not None:
                self.screen.blit(self.surf[index], (self.realX, self.realY))