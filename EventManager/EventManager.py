import pygame
from WindowOverlayHelper.WindowObject import WindowObject
from EventManager.EventArgs import *
from copy import deepcopy, copy

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
            "mouseScrollUp" : list(),             # only on first scroll up
            "mouseScrollDown" : list(),           # only on first scroll down
            "mouseOnUpAlways" : list(),           # always on mouse up
            "mouseDownAlways" : list(),           # always on mouse down

            # === keyboard ===
            "keyDown": list(),                  # on every key down
            "keyPress": list(),                 # only first key down until its reset
            "keyUp" : list(),                    # only on first key up
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
            "mouseScrollUp" : 0,
            "mouseScrollDown" : 0,
            "mouseOnUpAlways" : 0,
            "mouseDownAlways" : 0,        
            "keyDown": 1,             
            "keyPress": 1,           
            "keyUp" : 1,                
        }

        # add for mouse left, middle and right
        for side in ["Left", "Middle", "Right"]:
            self.argsCorrespondingToFunctions["mouseOnClick" + side] = 0
            self.argsCorrespondingToFunctions["mouseOnUp" + side] = 0
            self.argsCorrespondingToFunctions["mouseDown" + side] = 0

        # register self
        self.registerEvent(self.windowParent)

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
            if method == "eventManager" and obj != self.windowParent:
                self.subManagerObjects.append(obj)

                # pass event args on
                obj.eventManager.setMouseEventArgs(self.mouseEventArgs)
                obj.eventManager.setKeyboardEventArgs(self.keyboardEventArgs)

            # if methode and in known events
            if callable(getattr(obj, method)) and method in self.allEvents:
                self.allEvents[method].append(obj) # obj passed as pointer so memory will be okay

        # self.calcObjectPixelMap()

    def unregisterEvent(self, obj: WindowObject):
        """
        EventManager.unregisterEvent:
        - removes object from all events

        WindowObject obj: object to be removed

        return None
        """

        for method in dir(obj):
            if method.startswith("__"):
                continue

            if method == "eventManager" and obj != self.windowParent:
                self.subManagerObjects.remove(obj)

            if callable(getattr(obj, method)) and method in self.allEvents:
                self.allEvents[method].remove(obj)
                
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

# update event args ===========================================================================================================================================
    def updateMouseEventArgs(self, dt: float, mouse: pygame.mouse):
        """
        EventManager.updateMouseEventArgs:
        - update mouse args

        float dt: delta time
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
                self.mouseEventArgs.mouseClicked[i] = False
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

        self.mouseEventArgs.pos = (self.mouseEventArgs.x, self.mouseEventArgs.y)

        if self.mouseEventArgs.clicked == True:
            if mouse.get_pressed(num_buttons=3) == (0, 0, 0):
                print("here")

    def updateMouseScroll(self, event):
        self.mouseEventArgs.scroll = event.y

    def clearKeyboardEventArgs(self):
            """
            EventManager.resetEventArgs:
            - resets all keyboard event args

            return None
            """

            self.mouseEventArgs.scroll = 0

            self.keyboardEventArgs.pressed = set()
            self.keyboardEventArgs.down = set()
            self.keyboardEventArgs.up = set()

            key: KeyEventArgs
            for key in self.keyboardEventArgs.keys.values():
                key.pressed = False
                key.down = False
                key.up = False 

    def updateKeyboardEventArgsDOWN(self, downEvent):
        """
        EventManager.updateKeyboardEventArgsDOWN
        - updates Keyboard Args for down

        list keyboard: all keyboard events
        """

        down = downEvent.key

        if down not in self.keyboardEventArgs.keys:
            k = KeyEventArgs()
            k.unicode = downEvent.unicode

            self.keyboardEventArgs.keys[down] = k

        k: KeyEventArgs

        k = self.keyboardEventArgs.keys[down]
        k.unicode = downEvent.unicode

        k.down = True

        if k.holding == -1:
            k.holding = 0
            k.pressed = True
            k.sinceLastPress = -1

            self.keyboardEventArgs.pressed.add(k)

    def updateKeyboardEventArgsUP(self, upEvent):
        """
        EventManager.updateKeyboardEventArgsUP
        - updates Keyboard Args for up

        Event upEvent: pygame event.UP
        """

        up = upEvent.key

        if up not in self.keyboardEventArgs.keys:
            print("CRITICAL ERROR: Key not in keys")
            return

        k: KeyEventArgs
        k = self.keyboardEventArgs.keys[up]

        k.up = True
        k.holding = -1
        self.keyboardEventArgs.up.add(up)

    def updateKeyboardEventArgsDt(self, dt: float):
        """
        EventManager.updateKeyboardEventArgsDt
        - updates Keyboard Args (key.holding, key.sinceLastPress)

        float dt: detla time
        """

        key: KeyEventArgs
        for key in self.keyboardEventArgs.keys.values():
            if key.holding != -1:
                key.holding += dt
                self.keyboardEventArgs.down.add(key)

            if key.sinceLastPress < 0:
                key.sinceLastPress = 0
            else:
                key.sinceLastPress += dt

# check for trigger Events ===========================================================================================================================================
    def triggerRegisterdEvents(self):
        """
        EventManager.triggerRegisterdEvents:
        - updates all objects (depended on its event properties)
        - update sub EventManagers of objects

        return None
        """

        oldHover = self.mouseEventArgs.hovered.copy()
        self.mouseEventArgs.hovered.clear()

        for event in self.triggerEvents:
            correspondingArgs = self.argsList[self.argsCorrespondingToFunctions[event]]

            self.runEvent(event, correspondingArgs)

        # == for hover mechanic ==
        for hoveredObj in self.mouseEventArgs.hovered:
            if hoveredObj not in oldHover:
                if hasattr(hoveredObj, "mouseEnter"):
                    getattr(hoveredObj, "mouseEnter")(self.mouseEventArgs)
            else:
                oldHover.remove(hoveredObj)

        for notHoverdAnymore in oldHover:
            if hasattr(notHoverdAnymore, "mouseLeave"):
                    getattr(notHoverdAnymore, "mouseLeave")(self.mouseEventArgs)

    def runEvent(self, event, correspondingArgs, runSelf = True) -> bool:
        """
        EventManager.runEvent:
        - run events for this obj and sub event managers

        str event: name of event
        args correspondingArgs: corresponding args

        return bool
        - if it should stop current cycle because of WindowObject.onlyEventItemInForeground
        """

        if self.windowParent.events == False:
            return

        mouseEvent = type(correspondingArgs) == MouseEventArgs

        if mouseEvent and not self.windowParent.getRealRect().collidepoint(self.mouseEventArgs.pos) and not event.endswith("Always"):
            return False
        
        # run event for all sub objects
        for obj in sorted(self.subManagerObjects, key = lambda x: x.z, reverse=True):
            if obj.eventManager.runEvent(event, correspondingArgs, False):
                    return True

        # sort objects
        objects = sorted(self.allEvents[event], key = lambda x: x.z, reverse=True)

        # put self at back
        if self.windowParent in objects:
            objects.remove(self.windowParent)

            # important for sub manager, so that an object isnt run more then once
            if runSelf:
                objects.append(self.windowParent)

        obj: WindowObject
        for obj in objects:
            if obj.events == False:
                return

            # mouse is not on object
            if mouseEvent and not obj.getRealRect().collidepoint(self.mouseEventArgs.pos) and not event.endswith("Always"):
                continue

            # for hover since its special
            if event == "mouseEnter" or event == "mouseLeave" or event == "mouseHover":
                if obj not in self.mouseEventArgs.hovered:
                    self.mouseEventArgs.hovered.append(obj)

                if not event == "mouseHover":
                    continue

            # execute function
            getattr(obj, event)(copy(correspondingArgs))

            # if object is only obj to be called then break
            if mouseEvent and obj.onlyEventItemInForeground:
                return True
        
        return False

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
    
    def _mouseOnUpAlways(self) -> bool:
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
    
    def _mouseDownAlways(self) -> bool:
        return self._mouseDownLeft() or self._mouseDownMiddle() or self._mouseDownRight()

    def _mouseDownLeft(self) -> bool:
        return self.mouseEventArgs.mouseHolding[0] >= 0
    
    def _mouseDownMiddle(self) -> bool:
        return self.mouseEventArgs.mouseHolding[1] >= 0
    
    def _mouseDownRight(self) -> bool:
        return self.mouseEventArgs.mouseHolding[2] >= 0
    
    # == hover == -> have to be checked every cycle sadly, since opjects can move around freely, so it isnt dependend on user input :(

    def _mouseHover(self) -> bool:
        return True

    def _mouseEnter(self) -> bool:
        return True

    def _mouseLeave(self) -> bool:
        return True
    
    # == mouse scroll ==

    def _mouseScrollUp(self) -> bool:
        return self.mouseEventArgs.scroll > 0
    
    def _mouseScrollDown(self) -> bool:
        return self.mouseEventArgs.scroll < 0

    # == keyboard ==

    def _keyDown(self) -> bool:
        return len(self.keyboardEventArgs.down) > 0

    def _keyPress(self) -> bool:
        return len(self.keyboardEventArgs.pressed) > 0

    def _keyUp(self) -> bool:
        return len(self.keyboardEventArgs.up) > 0