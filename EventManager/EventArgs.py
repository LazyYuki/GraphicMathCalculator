class MouseEventArgs:
    def __init__(self) -> None:
        """
        MouseEventArgs:

        bool clicked: if mouse got clicked (button doesnt matter)
        bool up:on mouse button up (button doesnt matter)

        list sinceLastClick: list of "left, middle, right" mb -> time since last click (0 = clicked)
        list mouseHolding: list of "left, middle, right" mb -> time of continues holding (-1 not hold)
        list mouseClicked: list of "left, middle, right" mb -> which one got clicked (click = mouse only on first down)
        list mouseUp: list of "left, middle, right" mb -> which one got up

        float x: pos of mouse
        float y: pos of mouse
        float lastX: pos of mouse in last cycle
        float lastY: pos of mouse in last cycle

        list hovered: list of all currently hoverd objects
        """

        self.clicked = False
        self.up = False

        self.sinceLastClick = [1, 1, 1]                     #left, middle, right    # 0 = down
        self.mouseHolding = [-1, -1, -1]                    #left, middle, right    # time of continiues holding
        self.mouseClicked = [False, False, False]          #left, middle, right
        self.mouseUp = [False, False, False]               #left, middle, right#left, middle, right

        self.x = 0
        self.y = 0

        self.lastX = 0
        self.lastY = 0

        self.pos = (0, 0)

        self.hovered = []
    
class KeyboardEventArgs:
    def __init__(self) -> None:
        self.keys = {}

        self.keysDown = {}
        self.keysPress = {}
        self.keysUp = {}