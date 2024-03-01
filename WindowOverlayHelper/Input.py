class Input:
    def __init__(self, events: list):
        """
        Input constructor:
        - Class that contains all needed input from the user for the update methode

        list events: all pygame events

        return none
        """

        # === vars ===
        self.quit = False
        self.mouse = Mouse()

        # === interpret ===

        pass

class Mouse:
    def __init__(self) -> None:
        """
        Mouse constructor:
        - contains all events conserning the mouse

        return none
        """

        self.leftButton = False
        self.rightButton = False
        self.middleButton = False

        self.x = None
        self.y = None