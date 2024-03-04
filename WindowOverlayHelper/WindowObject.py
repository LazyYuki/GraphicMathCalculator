from EventManager.Input import Input

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

        # === properties ===
        self.screen = screen
        self.x = x
        self.y = y
        self.z = z # z = 0 foreground
        self.width = width
        self.height = height

        self.parent = None
        self.realX = x
        self.realY = y
        self.realS = x + width      # combination of x and width    | == end coord + 1
        self.realT = y + height     # combination of y and height   | == end coord + 1

        # === event ====
        self.show = True                # if it should be drawn
        self.events = True              # if it should run events

    def calcRealPosition(self):
        """
        WindowObject.calcRealPosition:
        - Calculates real position in reference to parent 

        return None
        """

        if self.parent != None:
            self.realX = self.parent.realX + self.x
            self.realY = self.parent.realY + self.y

            self.realS = min(self.width + self.realX, self.parent.realS)
            self.realT = min(self.height + self.realY, self.parent.realT)

    def getSpecialAreaLimit(self, x: int, y: int) -> bool:
        """
        WindowObject.specialAreaLimit:
        - tells if x and y are part of this object
        - needed if object is not a rect

        int x : real x position (like self.realX)
        int y : real y position (like self.realY)

        return bool
        - True if x and y are part of object
        """

        return (x >= self.realX and y >= self.realY and x < self.realS and y < self.realT)

    # def update(self, inp: Input):
    #     """
    #     WindowObject.update:
    #     - Updates every frame and calculates new positions and other stuff

    #     Input inp: input from pygame

    #     return None
    #     """

    #     pass

    def render(self):
        """
        WindowObject.render:
        - Updates every frame and draws everything

        return None
        """

        pass