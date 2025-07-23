from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskplanner import db
from flaskplanner.models import Event, Task 
from flaskplanner.task.forms import TaskForm

task = Blueprint('tasks', __name__)

@task.route("/addevent", methods=["GET", "POST"])
@login_required
def addevent():
    # check if post is submitted. 
    if request.method == "POST":

        # gets all the inputs from the form. 
        title = request.form.get("title")
        start = request.form.get("start")
        end = request.form.get("end")
        description = request.form.get("description")
        
        # Create a new Event object using the form data + current user's ID
        new_event = Event(title=title, start=start, end=end, description=description, user_id=current_user.id)
        db.session.add(new_event)
        db.session.commit()

        # after dding the event, it redirects user to the calendar page, 
        flash("Event added to calendar!", "success")
        return redirect(url_for("tasks.calendar"))

    return render_template("addevent.html")

@task.route('/addtask', methods=["GET", "POST"])
def addtask():

    form = TaskForm()
    
    if form.validate_on_submit():

        task = Task(
            title=form.title.data,
            date=form.date.data,
            description=form.description.data,
            type=form.type.data,
            user_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        flash("Task added to calendar!", "success")
        return redirect(url_for("tasks.calendar"))

    return render_template("addtask.html", form=form)

@task.route("/calendar")
@login_required
def calendar():
    events = Event.query.filter_by(user_id=current_user.id).all()
    tasks = Task.query.filter_by(user_id=current_user.id).all()

    json_events = []

    for event in events:
        json_events.append({
            "id": f"event-{event.id}",
            "title": f"[Event] {event.title}",
            "start": event.start,
            "end": event.end,
            "description": event.description or "",
            "color": "#4285F4"
        })

    for task in tasks:
        json_events.append({
            "id": f"task-{task.id}",
            "title": f"[Task] {task.title}",
            "start": str(task.date),
            "description": task.description or "",
            "type": task.type,  # <-- Add this!
            "color": "#34A853"
        })

    return render_template("calendar.html", title="Calendar", events=json_events)

@task.route("/delete_event/<int:event_id>", methods=["POST"])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)

    # Check ownership
    if event.user_id != current_user.id:
        abort(403)  # Forbidden

    db.session.delete(event)
    db.session.commit()
    return {"success": True}

@task.route("/delete_task/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    task_obj = Task.query.get_or_404(task_id)

    if task_obj.user_id != current_user.id:
        abort(403)

    db.session.delete(task_obj)
    db.session.commit()
    return {"success": True}


