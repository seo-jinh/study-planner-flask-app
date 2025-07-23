#__init__.py tells Python: “this folder is a package.” therefore all python folder needs to have this to run it 

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail            
from dotenv import load_dotenv
from flask_migrate import Migrate

load_dotenv()  # loads variables from .env

# Initialize extensions globally, not yet linked to flask app create reusable tools, 
# but they're not connected to any specific Flask app yet
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'         # redirects to login for @login_required
login_manager.login_message_category = 'info'    # Bootstrap alert style
mail = Mail()                                    # creates an instance of Flask-Mail, Send emails from your app using SMTP 

def create_app():

    # It's like storing a value to a variable, you need to return for it to give you a value
    app = Flask(__name__)   # Creates the Flask app, have to return later to run it. 

    # Configure from env
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
    app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

    # Attach extensions to the app, enables you to import db or mail in other files
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate = Migrate(app, db)

    # Each of these lines imports a Blueprint object defined in its routes.py file.
    # Register Blueprints (modular structure). Brings all routes from each routes.py file
    from flaskplanner.user.routes import users
    from flaskplanner.main.routes import main
    from flaskplanner.task.routes import task
    from flaskplanner.error.handlers import errors
    
    # actually links it so you can use the blueprints 
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(task)
    app.register_blueprint(errors)

    # starts the app.
    return app