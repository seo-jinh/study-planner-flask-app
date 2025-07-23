# models.py creates all the database models 
# from planner = imports from __init__.py - where it runs all the apps and initialization of instances 
# token is a secure, encoded string used to identify or authorize something — usually without storing sensitive info directly

from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer  # Used for generating secure password reset tokens.
from flaskplanner import db, login_manager                              # importing SQLAlchemy & login manager instance created in init
from flask import current_app
from flask_login import UserMixin
from itsdangerous import BadData

# WHEN TO IMPORT DB - A) Define database models,  B) Interact with the database directly, 
# extension expects user models to have certain attributes and methods.
# registers the function below as the function Flask-Login will use to load a user from the database when a user is logged in

@login_manager.user_loader  
def load_user(user_id):                  # loads when it needs to know which user it is by using user_id
    return User.query.get(int(user_id))  # gets the user with the primary_key 

# SQL alchemy allows database structure as classes and is referenced as models
# Structure for the database Model, holds users data
# db.model = base class from SQAlchemy gives user abilitiy to define columns, relationships and talk to database 
# UserMixin is from flask_login gives User default implementations of: .is_authenticated, .is_active, .get_id()
# This class inherits database from db.model, and login features from USerMixin

class User(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key = True)                                    # Creates Unique ID for user
    username = db.Column(db.String(20), unique = True, nullable= False)
    email = db.Column(db.String(120), unique = True, nullable= False)
    image_file =  db.Column(db.String(20), nullable= False, default = 'default.jpg')  # if user doenst have a pfp, provides with a default pfp
    password = db.Column(db.String(60), nullable=False)         
    events = db.relationship('Event', backref='user', lazy=True)                      # links User's Unique ID to tasks and events just for that user

    # Email and Password Reset, default is 30 minutes 
    # method attached to the User class
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})     # Converts the user’s ID into a secure token string, can be sent to the user via email as part of a reset link

    # Means this method doesn’t use self
    @staticmethod 
    def verify_reset_token(token, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=expires_sec)
            user_id = data['user_id']
        except BadData:       # If token is expired, tampered, or invalid, this prevents a crash and just returns None
            return None 
        return User.query.get(user_id)
    
    # gets user with that user ID ueful for debugging. 
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# creates a database called evenet that lives in sql that captures all the fields below. 
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start = db.Column(db.String(100), nullable=False)
    end = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(50))