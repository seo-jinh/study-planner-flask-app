
from flaskplanner import create_app  # imports the factory function

app = create_app()  # builds and configures it (routes, extensions, env variables, etc.)

if __name__ == '__main__':
    app.run(debug=True)  # only run if script executed directly, not when imported, only runs when you type python run.py
