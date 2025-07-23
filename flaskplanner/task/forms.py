from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired


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