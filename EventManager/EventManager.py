import pygame
from WindowOverlayHelper.WindowObject import WindowObject
from EventManager.EventArgs import KeyboardEventArgs, MouseEventArgs
from copy import deepcopy

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
            "mouseDown" : list(),                 # always when mouse hold
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
            self.allEvents["mouseDown" + side] = list()

        # events that will be triggerd in the current cycle
        self.triggerEvents = []

        # all sub event managers are saved here
        self.subManagerObjects = []

        # event Args - can be pointer from parent manager
        self.mouseEventArgs = MouseEventArgs()          # args || or Pointer to current Mouse Event Args        (if child event manager)
        self.keyboardEventArgs = KeyboardEventArgs()      # args || or Pointer to current Keyboard Event Args     (if child event manager)

        self.argsList = [self.mouseEventArgs, self.keyboardEventArgs]

        # number corresponds to index in list
        self.argsCorrespondingToFunctions = {
            "mouseOnClick" : 0,              
            "mouseOnUp" : 0,               
            "mouseDown" : 0,            
            "mouseHover" : 0,        
            "mouseEnter" : 0,         
            "mouseLeave" : 0,         
            "keyDown": 1,             
            "keyPress": 1,           
            "keyUP" : 1,                
        }

        # add for mouse left, middle and right
        for side in ["Left", "Middle", "Right"]:
            self.argsCorrespondingToFunctions["mouseOnClick" + side] = 0
            self.argsCorrespondingToFunctions["mouseOnUp" + side] = 0
            self.argsCorrespondingToFunctions["mouseDown" + side] = 0

        # object pixel map (every pixel gets assigned its corresponding object or multiple objects) - can be pointer from parent manager
        self.objectPixelMap = [[[] for x in range(self.windowParent.width)] for y in range(self.windowParent.height)]               # all objects in that position

# register event and helper ================================================================================================================================================

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
                obj.eventManager.setObjectPixelMap(self.objectPixelMap)

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
        self.argsList[0] = mEvent

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
        self.argsList[1] = kEvent

        sub: EventManager
        for sub in self.subManagerObjects:
            sub.eventManager.setKeyboardEventArgs(kEvent)

    def setObjectPixelMap(self, objectPixelMap: list):
        """
        EventManager.setObjectPixelMap:
        - updates pixel map for every sub event Manager

        list objectPixelMap: the normal object pixel map
        list objectPixelMapForeground: where only the foreground objects count

        return None
        """

        # set
        self.objectPixelMap = objectPixelMap

        # set for every sub manager
        for sub in self.subManagerObjects:
            sub.eventManager.setObjectPixelMap(objectPixelMap)

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
                if self.windowParent not in self.objectPixelMap[y][x]:
                    self.objectPixelMap[y][x].insert(0, self.windowParent)

                # check if objects are also in this area
                obj: WindowObject
                for obj in objects:
                    if obj.getSpecialAreaLimit(x, y) and obj not in self.objectPixelMap[y][x]:
                        self.objectPixelMap[y][x].insert(0, obj)

        # calcl for rest
        for sub in self.subManagerObjects:
            sub.eventManager.calcObjectPixelMap()

# update event args ===========================================================================================================================================
    def updateEventArgs(self, dt: float, pygameEvents: list, mouse: pygame.mouse):
        """
        EventManager.updateEventArgs:
        - updates event args based on pygame Events

        float dt: delta time
        list pygameEvents: all pygameEvents
        pygame.mouse mouse: mouse with events
        
        return None
        """

        # === mouse ===
        buttons = mouse.get_pressed(num_buttons=3)

        # loop through buttons
        for i in range(3):

            if buttons[i]:
                self.mouseEventArgs.sinceLastClick[i] = 0

                # mouse down and click
                if self.mouseEventArgs.mouseHolding[i] >= 0:
                    self.mouseEventArgs.mouseHolding[i] += dt
                    self.mouseEventArgs.mouseClicked[i] = False

                else:
                    self.mouseEventArgs.mouseHolding[i] = 0
                    self.mouseEventArgs.mouseClicked[i] = True
            else:
                # up
                if self.mouseEventArgs.mouseHolding[i] >= 0:
                    self.mouseEventArgs.mouseUp[i] = True
                    self.mouseEventArgs.mouseHolding[i] = -1 # reset
                else:
                    self.mouseEventArgs.mouseUp[i] = False

                self.mouseEventArgs.sinceLastClick[i] += dt

        # calc if clicked
        self.mouseEventArgs.clicked = sum(self.mouseEventArgs.mouseClicked) > 0
        self.mouseEventArgs.up = sum(self.mouseEventArgs.mouseUp) > 0

        # mouse pos
        self.mouseEventArgs.lastX = self.mouseEventArgs.x
        self.mouseEventArgs.lastY = self.mouseEventArgs.y

        self.mouseEventArgs.x, self.mouseEventArgs.y = mouse.get_pos()

        # === keyboard === TODO

# check for trigger Events ===========================================================================================================================================
    def triggerRegisterdEvents(self):
        """
        EventManager.triggerRegisterdEvents:
        - updates all objects (depended on its event properties)
        - update sub EventManagers of objects

        return None
        """

        # TODO auf foreground und so shit achten
        # TODO auf bounderies achten und so

        for event in self.triggerEvents:
            correspondingArgs = self.argsList[self.argsCorrespondingToFunctions[event]]

            for obj in self.allEvents[event]:
                # getattr(obj, event)(correspondingArgs)
                getattr(obj, event)(deepcopy(correspondingArgs)) # slower but for safety

        # TODO: run on all sub event managers, but firstly connect bn


    def updateCurrentTriggerEvents(self):
        """
        EventManager.updateCurrentTriggerEvents:
        - checks which events have to be triggerd

        return None
        """

        self.triggerEvents = []

        for key in self.allEvents.keys():
            funcName = "_" + key
            if hasattr(self, funcName) and getattr(self, funcName)():
                self.triggerEvents.append(key)

# === all events === TODO: für jedes event in self.allEvents den shit schreiben
    
    # == mouse clicked ==

    def _mouseOnClick(self) -> bool:
        return self.mouseEventArgs.clicked
    
    def _mouseOnClickLeft(self) -> bool:
        return self.mouseEventArgs.mouseClicked[0]
    
    def _mouseOnClickMiddle(self) -> bool:
        return self.mouseEventArgs.mouseClicked[1]
    
    def _mouseOnClickRight(self) -> bool:
        return self.mouseEventArgs.mouseClicked[2]
    
    # == mouse up ==

    def _mouseOnUp(self) -> bool:
        return self.mouseEventArgs.up
    
    def _mouseOnUpLeft(self) -> bool:
        return self.mouseEventArgs.mouseUp[0]
    
    def _mouseOnUpMiddle(self) -> bool:
        return self.mouseEventArgs.mouseUp[1]
    
    def _mouseOnUpRight(self) -> bool:
        return self.mouseEventArgs.mouseUp[2]
    
    # == mouse down ==

    def _mouseDown(self) -> bool:
        return self._mouseDownLeft() or self._mouseDownMiddle() or self._mouseDownRight()

    def _mouseDownLeft(self) -> bool:
        return self.mouseEventArgs.mouseHolding[0] >= 0
    
    def _mouseDownMiddle(self) -> bool:
        return self.mouseEventArgs.mouseHolding[1] >= 0
    
    def _mouseDownRight(self) -> bool:
        return self.mouseEventArgs.mouseHolding[2] >= 0
    
# TODO: implement hover somehow :shrug: