import pygame

### generate basic pygame structure without comments

screen = pygame.display.set_mode((1200, 800))

while True:
    events = pygame.event.get()
    for event in events:
        match event.type:
            case pygame.QUIT:
                break

            case pygame.KEYDOWN:
                print(event.key)

            case pygame.KEYUP:
                print(event.key)

    pygame.display.flip()