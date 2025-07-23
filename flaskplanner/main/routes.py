from flask import Blueprint, render_template, url_for
from flask_login import current_user, login_required
from datetime import date
from flaskplanner.models import Task, Event
from sqlalchemy import func

main = Blueprint('main', __name__)
@main.route("/")
@main.route("/home")

@login_required
def home():
    today = date.today()
    events_today = Event.query.filter(Event.user_id == current_user.id,
    func.date(Event.start) == today).all()
    tasks_today = Task.query.filter_by(user_id=current_user.id, date=today).all()

    # Load user’s current profile picture
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('home.html', image_file=image_file, tasks_today = tasks_today,events_today=events_today,title ='Home')


@main.route("/timer")
@login_required
def timer():
    return render_template('timer.html',title ="Timer")

