# TODO: better import name structure... WTF is application.application??
from application.application import Application, ApplicationSettings

from WindowOverlayHelper.Window import Window
from WindowOverlayHelper.WindowObject import WindowObject
from EventManager.Input import Input
from UIElements.test import Test

window1 = Window(0, 0, 0, 0, 0, 0)
window2 = Window(0, 0, 0, 0, 0, 0)
window3 = Window(0, 0, 0, 0, 0, 0)

window2.addObject(window3)
window1.addObject(window2)

window1.eventManager.mouseEventArgs.clicked = True

# TODO: better integration between Application - WindowOverlayHelper components
# ... maybe move everything to the application class?

settings = ApplicationSettings("Graphic math calculator", 1200, 800, 60)

app = Application(settings)
if __name__ == "__main__":
    app.launch()
