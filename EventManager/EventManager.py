from enum import Enum
from EventManager.Input import Input
from WindowOverlayHelper.WindowObject import WindowObject

class MouseEventArgs:
    def __init__(self) -> None:
        self.clicked = False

        self.leftButton = False
        self.rightButton = False
        self.middleButton = False

        self.x = 0
        self.y = 0

        self.lastX = 0
        self.lastY = 0
    
class KeyboardEventArgs:
    def __init__(self) -> None:
        self.keys = {}

class EventProperties:
    pass

class IndividuelEventProperties:
    pass

class Event():
    mouseEventArgs = 0
    keyboardEventArgs = 1

    events = {
        # === mouse ===
        "mouseOnClick" : mouseEventArgs,              # only first mouse click until its reset
        "mouseOnClickLeft" : mouseEventArgs,          # only first left mouse click until its reset
        "mouseOnClickRight" : mouseEventArgs,         # only first right mouse click until its reset
        "mouseOnClickMiddle" : mouseEventArgs,        # only first middle mouse click until its reset
        "mouseHover" : mouseEventArgs,                # on every hover
        "mouseEnter" : mouseEventArgs,                # only on first hover 
        "mouseLeave" : mouseEventArgs,                # only on first leave

        # === keyboard ===
        "keyDown" : keyboardEventArgs,                # on every key down
        "keyPress" : keyboardEventArgs,               # only first key down until its reset
        "keyUP" : keyboardEventArgs,                  # only on first key up
    }

class EventManager:
    def __init__(self) -> None:
        """
        EventManager Constructor:
        - stores all events
        - triggers all stored events

        return None
        """

        self.allEvents = {
            # "mouseOnClick": [object, EventProperties]
        }

        self.eventProperties = EventProperties()

        pass

    def registerEvent(self, obj: WindowObject) -> list:
        """
        EventManager.registerEvent:
        - checks object for all registered events
        - safes it to the current class

        WindowObject obj: pointer to check object

        return list
        - list of all found events
        """

        pass

    def triggerRegisterdEvents(self, inp: Input):
        """
        EventManager.triggerRegisterdEvents:
        - calculates all updates for events
        - updates all objects (depended on its event properties)

        Input inp: all pygame events compiled

        return None
        """

        pass