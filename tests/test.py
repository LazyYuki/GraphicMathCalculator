import pygame
from UIElements.Rect import RotatableRect
from math import sin, radians
### generate basic pygame structure without comments

screen = pygame.display.set_mode((1200, 800))

clock = pygame.time.Clock()

r1 = RotatableRect(screen, 100, 100, 0, 100, 100, color=(255, 0, 0), borderRadius=10, borderWidth=3)
r2 = RotatableRect(screen, 100, 100, 0, 100, 100, color=(0, 255, 0), borderRadius=10, borderWidth=3)

r1.setAngle(-45)

r1.realX = sin(radians(r1.angle)) * r1.width + r1.x
r1.realY = sin(radians(90 - r1.angle)) * r1.height + r1.y - r1.height

print(r1.realX, r1.realY)

angle = 0
while True:
    clock.tick(60)

    events = pygame.event.get()
    for event in events:
        match event.type:
            case pygame.QUIT:
                pygame.quit()
                exit()
                break

    r1.render()
    r2.render()

    pygame.display.flip()

# import os

# def fast_scandir(dirname):
#     subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
#     for dirname in list(subfolders):
#         subfolders.extend(fast_scandir(dirname))
#     return subfolders

# print(fast_scandir("Apps"))
# print([f.path for f in os.scandir("Apps/Algebra/Matrix") if f.is_file()])
