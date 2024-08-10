import warnings, pygame

from EventManager.EventManager import EventManager
from WindowOverlayHelper.WindowObject import WindowObject

class Window(WindowObject):
    def __init__(self, screen, x: int, y: int, z: int, width: int, height: int):
        """
        Window constructor: 
        - Represents an container for sub objects (WindowObject.py) to be renders and stored.
        - The objects will only be shown in the renderd width / height
        
        pointer screen: pointer to screen from pygame
        int x: x coord relative to parent
        int y: y coord relative to parent
        int z: z coord (important for foreground and background draw)
        int width: width coord relative to parent
        int height: height coord relative to parent

        return None
        """

        super().__init__(screen, x, y, z, width, height)
        
        # contains all objects from WindowObject
        self.objects = []

        # color
        self.showColor = False
        self.color = (0, 0, 0)

        # set event manager
        self.eventManager = EventManager(self)
        
    def addObject(self, obj: WindowObject) -> bool:
        """
        Window.addObject:
        - adds Object to Window render list
        - checks if obj is WindowObject or child from WindowObject

        WindowObject obj: object to be pastet

        return bool
        - if adding the object succeded or not
        """

        # TODO: getAllBases for finding WindowObject of Parent Parent... kms pls

        # check if obj is WindowObject or child of it
        #if obj.__class__.__bases__.count(WindowObject) + (obj.__class__ == WindowObject) == 0 or obj == self:
        if obj == self:
            warnings.warn("Object cant be added to itself.")
            return False

        if not issubclass(obj.__class__, WindowObject):
            warnings.warn("Object is not WindowObject or child of it.")
            return False

        # check if it has parent already
        if obj.parent != None:
            warnings.warn("Object already has a parent.")
            return False

        # set parent
        obj.parent = self

        # append to objects that are managed
        self.objects.append(obj)

        # calculate real Position
        obj.calcRealPosition()

        # register in event Manager
        self.eventManager.registerEvent(obj)

        return True
    
    def removeObject(self, obj: WindowObject) -> bool:
        """
        Window.removeObject:
        - removes Object from Window render list
        - checks if obj is WindowObject or child from WindowObject

        WindowObject obj: object to be removed

        return bool
        - if removing the object succeded or not
        """

        # check if obj is WindowObject or child of it
        if not issubclass(obj.__class__, WindowObject):
            warnings.warn("Object is not WindowObject or child of it.")
            return False

        # check if it has parent already
        if obj.parent != self:
            warnings.warn("Object is not child of this parent.")
            return False

        # set parent
        obj.parent = None

        # remove from objects that are managed
        self.objects.remove(obj)

        # register in event Manager
        self.eventManager.unregisterEvent(obj)

        return True

    def calcRealPosition(self):
        """
        WindowObject.calcRealPosition:
        - Calculates real position in reference to parent 
        - recalculates position of children too

        return None
        """

        super().calcRealPosition()

        # calc for every sub object too
        for obj in self.objects:
            obj.calcRealPosition()

    def hide(self, lockDraw = False, lockEvents = False):
        """
        Window.hide:
        - hide object from draw and all interaction if not locked
        - pass to children

        bool lockDraw: locks draw from changing
        bool lockEvents: locks events from changing

        return bool
        """

        if self.lockHide: return

        if not (self.lockDraw or lockDraw): 
            self.draw = False

            obj: WindowObject
            for obj in self.objects:
                obj.hide(False, True)

        if not ( self.lockEvents or lockEvents):
            self.events = False

            obj: WindowObject
            for obj in self.objects:
                obj.hide(True, False)

    def show(self, lockDraw = False, lockEvents = False):
        """
        Window.show:
        - show object from draw and all interaction if not locked
        - pass to children

        bool lockDraw: locks draw from changing
        bool lockEvents: locks events from changing

        return bool
        """

        if self.lockShow: return

        if not (self.lockDraw or lockDraw): 
            self.draw = True

            obj: WindowObject
            for obj in self.objects:
                obj.show(False, True)

        if not ( self.lockEvents or lockEvents):
            self.events = True

            obj: WindowObject
            for obj in self.objects:
                obj.show(True, False)

    def absoluteHide(self):
        """
        Window.absoluteHide:
        - hide object from draw and all interaction
        - pass to children
        """

        self.hide()
        self.lockShow = True

    def absoluteShow(self):
        """
        Window.absoluteHide:
        - hide object from draw and all interaction
        - pass to children
        """

        self.lockShow = False
        self.show()

    def update(self, dt: float):
        """
        WindowObject.update:
        - Updates every frame

        return None
        """
        # loop through objects and render
        obj: WindowObject
        for obj in self.objects:
            obj.update(dt)

        for obj in self.objects:
            obj.update(dt)

    def idCheck(self, id):
        o: WindowObject
        for o in self.objects:
            if o.ID == id:
                return o
            
        return None

    def render(self):
        """
        WindowObject.render:
        - Updates every frame and draws everything

        return None
        """

        if self.draw == False:
            return

        if self.showColor:
            pygame.draw.rect(self.screen, self.color, self.getRealRect())

        # sort for z value (foreground / background draw) -> z = 0, foreground
        self.objects.sort(key= lambda x: x.z, reverse=True)

        # loop through objects and render
        obj: WindowObject
        for obj in self.objects:
            obj.render()

