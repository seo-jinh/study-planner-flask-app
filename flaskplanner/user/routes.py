from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskplanner import db, bcrypt
from flaskplanner.user.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskplanner.models import User                                 # gives me access to the user table in DB
from flaskplanner.user.utils import save_picture, send_reset_email   # functions from utils.py that handles emailing the user & saving images

# creates a blueprint object allows for the connection of all __init__.py files 
users = Blueprint('users', __name__)

# uses from flask_login import current_user, from flaskblog.users.forms import RegistrationForm, from flaskblog import bcrypt,
# When registered stores teh password  so it’s not stored in plaintext in your database(important for security)
# .decode('utf-8') → turns the hash (bytes) into a string so it can be saved into the database as text

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # this follows the formatting and requriements set in User class in models.py
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)                                   # adds the new user to the SQLAlchemy session (staging area for DB changes).
        db.session.commit()                                    # writes the new user to the database
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

# user query filter by comes from SQLalchemy, User inherits from db.Model
# lets me check if login is legit without ever exposing the real password  
@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))

# Route to update user account info (only accessible when logged in)
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()  # Imports and initializes update form from forms.py

    # validate_on_submit() is a shortcut for doing both: if request.method == 'POST' and form.validate():
    if form.validate_on_submit():
        if form.picture.data:                                # If user uploaded a new profile picture
            picture_file = save_picture(form.picture.data)   # Resize and save pic via utils.py
            current_user.image_file = picture_file           # Update current user's profile picture
        
        # Update username and email from form input
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()                                 # Commit changes to the database
        flash('Your account has been updated!', 'success')  # Show success message
        return redirect(url_for('users.account'))           # Prevent form resubmission on refresh

    # 'GET'-when user visits account page,'POST' when user updates the form page 
    # just displaying 'GET'(nonupdated) information if user didn't update anything. 
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    # Load user’s current profile picture
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    # Render the account page with current user info and profile picture
    return render_template('account.html', title='Account',image_file=image_file, form=form)

# uses send_reset_email() in utils.py where get_reset_token() is cled from models.py where it sends a link 
# rest are just formatting and flash message + render_template
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()               # imported from forms.py 
    if form.validate_on_submit():
        # don’t need to import the User class again in utils.py because the object you receive is already a full-blown User instance, created earlier by routes.py
        user = User.query.filter_by(email=form.email.data).first()      # searches the DB for a user with that email. user is now an instance with that email
        send_reset_email(user)                                          # Connected from utils.py, sends email
        flash('An email has been sent with instructions to reset your password.', 'info')   # utils.py does the rest
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

# KEY DIFFERENCE reset_password = they receive a link, reset_password<token> = when they click the link.
# Route for resetting a password using a secure token sent via email
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    # If user is already logged in, redirect them home
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    # Verify the token and get the user
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()

    # If form is submitted and valid, update the user's password
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))

    # If token is valid but form not submitted yet, show reset form
    return render_template('reset_token.html', title='Reset Password', form=form)