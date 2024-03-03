class MouseEventArgs:
    def __init__(self) -> None:
        self.clicked = False

        self.sinceLastClick = [0, 0, 0]     #left, middle, right
        self.sinceMouseDown = [-1, -1, -1]  #left, middle, right

        self.leftButton = False
        self.rightButton = False
        self.middleButton = False

        self.x = 0
        self.y = 0

        self.lastX = 0
        self.lastY = 0

        self.hovered = []
    
class KeyboardEventArgs:
    def __init__(self) -> None:
        self.keys = {}

        self.keysDown = {}
        self.keysPress = {}
        self.keysUp = {}