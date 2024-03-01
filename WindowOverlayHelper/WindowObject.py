from WindowOverlayHelper.Input import Input

class WindowObject():
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int) -> None:
        """
        WindowObject constructore:
        - An sub object that is drawn in a Window (Window.py)
        - All coordinates are relative to its parent Window

        pointer screen: pointer to screen from pygame
        int x: x coord relative to parent
        int y: y coord relative to parent
        int z: z coord (important for foreground and background draw)
        int width: width coord relative to parent
        int height: height coord relative to parent

        return: None
        """

        self.screen = screen
        self.x = x
        self.y = y
        self.z = z # z = 0 foreground
        self.width = width
        self.height = height

    def update(self, inp: Input):
        """
        WindowObject.update:
        - Updates every frame and calculates new positions and other stuff

        Input inp: input from pygame

        return None
        """

        pass

    def render(self):
        """
        WindowObject.render:
        - Updates every frame and draws everything

        return None
        """

        pass