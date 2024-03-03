import pygame
from EventManager.Input import Input
from WindowOverlayHelper.WindowObject import WindowObject
from EventManager.EventArgs import KeyboardEventArgs, MouseEventArgs

class Event():
    mouseEventArgs = 0
    keyboardEventArgs = 1

    events = [
        # === mouse ===
        "mouseOnClick",              # only first mouse click until its reset
        "mouseOnClickLeft",          # only first left mouse click until its reset
        "mouseOnClickRight",         # only first right mouse click until its reset
        "mouseOnClickMiddle",        # only first middle mouse click until its reset
        "mouseHover",                # on every hover
        "mouseEnter",                # only on first hover 
        "mouseLeave",                # only on first leave

        # === keyboard ===
        "keyDown",                  # on every key down
        "keyPress",                 # only first key down until its reset
        "keyUP",                    # only on first key up
    ]

class EventManager:
    def __init__(self, parent: WindowObject) -> None:
        """
        EventManager Constructor:
        - stores all events
        - triggers all stored events

        WindowObject parent: parent of event Manager

        return None
        """

        # parent
        self.windowParent = parent

        # saves all objects with the corresponding functions
        self.allEvents = {
            # === mouse ===
            "mouseOnClick" : list(),              # only first mouse click until its reset
            "mouseOnUp" : list(),                 # only first mouse click until its reset
            "mouseOnDown" : list(),                 # only first mouse click until its reset
            "mouseHover" : list(),                # on every hover
            "mouseEnter" : list(),                # only on first hover 
            "mouseLeave" : list(),                # only on first leave

            # === keyboard ===
            "keyDown": list(),                  # on every key down
            "keyPress": list(),                 # only first key down until its reset
            "keyUP" : list(),                    # only on first key up
        }

        # add for mouse left, middle and right
        for side in ["Left", "Middle", "Right"]:
            self.allEvents["mouseOnClick" + side] = list()
            self.allEvents["mouseOnUp" + side] = list()
            self.allEvents["mouseOnDown" + side] = list()

        # events that will be triggerd in the current cycle
        self.triggerEvents = []

        # all sub event managers are saved here
        self.subManagerObjects = []

        # event Args - can be pointer from parent manager
        self.mouseEventArgs = MouseEventArgs()          # args || or Pointer to current Mouse Event Args        (if child event manager)
        self.keyboardEventArgs = KeyboardEventArgs()      # args || or Pointer to current Keyboard Event Args     (if child event manager)

        # object pixel map (every pixel gets assigned its corresponding object or multiple objects) - can be pointer from parent manager
        self.objectPixelMap = [[None for x in range(self.windowParent.width)] for y in range(self.windowParent.height)]
        self.objectPixelOffsetX = 0
        self.objectPixelOffsetY = 0

    def registerEvent(self, obj: WindowObject):
        """
        EventManager.registerEvent:
        - checks object for all registered events
        - safes it to the current manager
        - checks for children EventManagers

        WindowObject obj: pointer to check object

        return None
        """

        # search all methodes and attributes of obj
        for method in dir(obj):
            # filter all "secrete" methods (with "__" at start) 
            if method.startswith("__"):
                continue

            # if object also includes a sub event Manager
            if method == "eventManager":
                self.subManagerObjects.append(obj)

                # pass event args on
                obj.eventManager.setMouseEventArgs(self.mouseEventArgs)
                obj.eventManager.setKeyboardEventArgs(self.keyboardEventArgs)

                # pass on objectPixelMap

                # TODO

            # if methode and in known events
            if callable(getattr(obj, method)) and method in self.allEvents:
                self.allEvents[method].append(obj) # obj passed as pointer so memory will be okay
                
    def setMouseEventArgs(self, mEvent: MouseEventArgs):
        """
        EventManager.setMouseEventArgs:
        - set mouse Event Args
        - set mouse Event Args for all sub Managers

        list pygameEvents: all pygameEvents

        return None
        """

        self.mouseEventArgs = mEvent

        for sub in self.subManagerObjects:
            sub.eventManager.setMouseEventArgs(mEvent)

    def setKeyboardEventArgs(self, kEvent: KeyboardEventArgs):
        """
        EventManager.setMouseEventArgs:
        - set mouse Event Args
        - set mouse Event Args for all sub Managers

        list pygameEvents: all pygameEvents

        return None
        """

        self.keyboardEventArgs = kEvent

        sub: EventManager
        for sub in self.subManagerObjects:
            sub.eventManager.setKeyboardEventArgs(kEvent)

    def setObjectPixelMap(self):
        pass

    def updateEventArgs(self, pygameEvents: list):
        """
        EventManager.updateEventArgs:
        - updates event args based on pygame Events

        list pygameEvents: all pygameEvents

        return None
        """

        pass

    def triggerRegisterdEvents(self):
        """
        EventManager.triggerRegisterdEvents:
        - updates all objects (depended on its event properties)
        - update sub EventManagers of objects

        return None
        """



        pass