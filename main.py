import pygame

from WindowOverlayHelper.Window import Window
from WindowOverlayHelper.WindowObject import WindowObject

from EventManager.Input import Input

from UIElements.test import Test

window1 = Window(0, 0, 0, 0, 0, 0)
window2 = Window(0, 0, 0, 0, 0, 0)
window3 = Window(0, 0, 0, 0, 0, 0)

window2.addObject(window3)
window1.addObject(window2)

window1.eventManager.mouseEventArgs.clicked = True

print(window3.eventManager.allEvents)

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