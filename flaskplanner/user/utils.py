# used to handle file uploads for user profiles
# UTIL IS USED IN users/routes.py -> from flaskblog.users.utils import save_picture, send_reset_email

import os                    # module for handling file paths and filenames
import secrets               # module to generate secure random values
from PIL import Image        # From Pillow library, Used to resize and process images
from flask import url_for, current_app      # Generates the URL to a route, Gives you access to the Flask app's config
from flask_mail import Message      # create an email message object with subject, body, and recipients
from flaskplanner import mail          # importing the mail = Mail() object you created in __init__.py


def save_picture(form_picture):
    # Generate a random filename, removes the original pg or png name since ther can be moultiple instance of that file name. 
    random_hex = secrets.token_hex(8)    # creates a secure random string like 'f8a3c9e1'
    _, f_ext = os.path.splitext(form_picture.filename)      # splits filename into name + extension
    picture_fn = random_hex + f_ext      # Combines them to make something like 'f8a3c9e1.jpg', avoids name collisions with existing files
    
    # This tells Flask to save the image in: /FlasK_Blog/flaskblog/static/profile_pics/<randomname>.jpg
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # Good to save storage and automatically resizes it 
    output_size = (125, 125)
    i = Image.open(form_picture)    # Open the uploaded image (form_picture) using Pillow, and assign it to a variable named i
    i.thumbnail(output_size)
    i.save(picture_path)

    # store that filename in the database (like user.image_file = picture_fn)
    return picture_fn


def send_reset_email(user):

    # Does NOT IMPORT USER FROM MODEL, routes.py already does that,it's just receiving a user object as an argument 
    # User imported in routes.py
    # Creates an instance of user 
    # don’t need to import the User class again in utils.py because the object you receive 
    # is already a full-blown User instance, created earlier by routes.py
    token = user.get_reset_token()  # a method from models.py 
    # only works after mail.init_app(app) is called 
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    
    # Doesn't need a redirect since you are just sending a link. Token is sent in the email 
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)