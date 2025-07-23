from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, TimeField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskplanner.models import User

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    description = TextAreaField('Description')
    type = SelectField('Type', choices=[
        ('Personal Work', 'Personal Work'),
        ('Club Work', 'Club Work'),
        ('Friends/Family', 'Friends/Family'),
        ('Homework', 'Homework'),
        ('Chores', 'Chores'),
        ('Fitness', 'Fitness'),
        ('Other', 'Other')
    ], default='Other')
    submit = SubmitField("Submit")