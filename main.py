# TODO: better import name structure... WTF is appli
from Application.Application import Application, ApplicationSettings

# TODO: better integration between Application - WindowOverlayHelper components
# ... maybe move everything to the application class

settings = ApplicationSettings("Graphic math calculator", 1200, 800, 60)

app = Application(settings)
if __name__ == "__main__":
    app.launch()
