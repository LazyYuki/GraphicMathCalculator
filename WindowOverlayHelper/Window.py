from WindowOverlayHelper.Input import Input
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
        
        self.__objects = [] # contains all objects from WindowObject

    def addObject(self, obj: WindowObject) -> bool:
        """
        Window.addObject:
        - adds Object to Window render list
        - checks if obj is WindowObject or child from WindowObject

        WindowObject obj: object to be pastet

        return bool
        - if adding the object succeded or not
        """

        if obj.__class__.__bases__.count(WindowObject) + (obj.__class__ == WindowObject) == 0 or obj == self:
            return False

        self.__objects.append(obj)

        return True

    def update(self, inp: Input):
        """
        WindowObject.update:
        - Updates every frame and calculates new positions and other stuff

        Input inp: input from pygame

        return None
        """

        pass

    def render(self):
        """
        WindowObject.render:
        - Updates every frame and draws everything

        return None
        """

        # sort for z value (foreground / background draw) -> z = 0, foreground
        self.__objects.sort(key= lambda x: x.z, reverse=True)

        # loop through objects and render
        obj: WindowObject
        for obj in self.__objects:
            obj.render()

