import pygame
from EventManager.Input import Input
from WindowOverlayHelper.WindowObject import WindowObject
from EventManager.EventArgs import KeyboardEventArgs, MouseEventArgs

"""
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
"""

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
        self.objectPixelMap = [[[] for x in range(self.windowParent.width)] for y in range(self.windowParent.height)]               # all objects in that position
        self.objectPixelMapForeground = [[None for x in range(self.windowParent.width)] for y in range(self.windowParent.height)]   # cares about the foreground of object

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
                obj.eventManager.setObjectPixelMap(self.objectPixelMap, self.objectPixelMapForeground)

            # if methode and in known events
            if callable(getattr(obj, method)) and method in self.allEvents:
                self.allEvents[method].append(obj) # obj passed as pointer so memory will be okay
                
    def setMouseEventArgs(self, mEvent: MouseEventArgs):
        """
        EventManager.setMouseEventArgs:
        - set mouse Event Args
        - set mouse Event Args for all sub Managers

        MouseEventArgs mEvent: mouse event args

        return None
        """

        self.mouseEventArgs = mEvent

        for sub in self.subManagerObjects:
            sub.eventManager.setMouseEventArgs(mEvent)

    def setKeyboardEventArgs(self, kEvent: KeyboardEventArgs):
        """
        EventManager.setKeyboardEventArgs:
        - set keyboard Event Args
        - set keyboard Event Args for all sub Managers

        KeyboardEventArgs kEvent: keyboard event args

        return None
        """

        self.keyboardEventArgs = kEvent

        sub: EventManager
        for sub in self.subManagerObjects:
            sub.eventManager.setKeyboardEventArgs(kEvent)

    def setObjectPixelMap(self, objectPixelMap: list, objectPixelMapForeground: list):
        """
        EventManager.setObjectPixelMap:
        - updates pixel map for every sub event Manager

        list objectPixelMap: the normal object pixel map
        list objectPixelMapForeground: where only the foreground objects count

        return None
        """

        # set
        self.objectPixelMap = objectPixelMap
        self.objectPixelMapForeground = objectPixelMapForeground

        # set for every sub manager
        for sub in self.subManagerObjects:
            sub.eventManager.setObjectPixelMap(objectPixelMap, objectPixelMapForeground)

    def calcObjectPixelMap(self):
        """
        EventManager.calcObjectPixelMap:
        - calculates the actual objects per pixel

        list objectPixelMap: the normal object pixel map
        list objectPixelMapForeground: where only the foreground objects count

        return None
        """
        
        # calc
        self.windowParent.calcRealPosition()

        # calculate object pixel
        rX, rY, rS, rT = self.windowParent.realX, self.windowParent.realY, self.windowParent.realS, self.windowParent.realT
        objects = self.windowParent.objects

        print(rX, rY, rS, rT)

        for y in range(rY, rT):
            for x in range(rX, rS):
                # set window parent to current foreground
                self.objectPixelMap[y][x].append(self.windowParent)
                self.objectPixelMapForeground[y][x] = self.windowParent

                # check if objects are also in this area
                obj: WindowObject
                for obj in objects:
                    if obj.getSpecialAreaLimit(x, y):
                        self.objectPixelMap[y][x].append(obj)
                        self.objectPixelMapForeground[y][x] = obj

        # calcl for rest
        for sub in self.subManagerObjects:
            sub.eventManager.calcObjectPixelMap()

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