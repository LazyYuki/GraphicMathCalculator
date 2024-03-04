import pygame

from WindowOverlayHelper.Window import Window
from WindowOverlayHelper.WindowObject import WindowObject

from EventManager.Input import Input

from UIElements.test import Test

window1 = Window(None, 0, 0, 0, 10, 10)
window2 = Window(None, 5, 5, 0, 5, 5)
window3 = Window(None, 0, 3, 0, 10, 3)
obj1 = WindowObject(None, 0, 1, 0, 3, 9)

window2.addObject(window3)
window1.addObject(window2)
#window1.addObject(obj1)

window1.eventManager.calcObjectPixelMap()

name1 = str(window1.eventManager.objectPixelMapForeground[0][0])
name2 = str(window1.eventManager.objectPixelMapForeground[5][5])
name3 = str(window1.eventManager.objectPixelMapForeground[5][8])
name4 = str(window1.eventManager.objectPixelMapForeground[0][1])

print(name1, name2, name3, name4)

for i in range(len(window1.eventManager.objectPixelMapForeground)):
    s = ""

    for j in range(10):
        s += str(window1.eventManager.objectPixelMapForeground[j][i]).replace(name1, "w1").replace(name2, "w2").replace(name3, "w3").replace(name4, "obj4") + " | "

    print(s)


exit(0)

# === variables === 
screenWidth = 800
screenHeight = 800
screen = None
clock = None
fps = 60
inp = None

# === init pygame ===
pygame.init()

screen = pygame.display.set_mode((screenWidth, screenHeight))

clock = pygame.time.Clock()

# === loop ===
while True:
    # loop through events
    events = pygame.event.get()

    inp = Input(events)

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        
    print(pygame.mouse.get_pos())

    # reset screen
    screen.fill((255, 255, 255))

    # get delta time
    dt = clock.tick(fps)

    # show fps
    currentFps = clock.get_fps()
    pygame.display.set_caption(f"FPS: {currentFps:.0f}")

    # update display
    pygame.display.flip()