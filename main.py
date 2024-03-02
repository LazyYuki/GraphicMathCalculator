import pygame
from WindowOverlayHelper.Window import Window
from WindowOverlayHelper.WindowObject import WindowObject
from EventManager.Input import Input

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


    # reset screen
    screen.fill((255, 255, 255))

    # get delta time
    dt = clock.tick(fps)

    # show fps
    currentFps = clock.get_fps()
    pygame.display.set_caption(f"FPS: {currentFps:.0f}")

    # update display
    pygame.display.flip()