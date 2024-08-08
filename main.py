from Application.Application import Application, ApplicationSettings

settings = ApplicationSettings("Graphic math calculator", 1200, 800, 60)

app = Application(settings)
if __name__ == "__main__":
    app.launch()
