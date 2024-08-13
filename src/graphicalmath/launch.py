from application import interface, settings

appSettings = settings.ApplicationSettings("Graphical Math", 1200, 800, 120)
app = interface.Application(appSettings)

if __name__ == "__main__":
    app.launch()