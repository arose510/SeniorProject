from flask import Blueprint, jsonify, render_template, request, flash
from flask_login import login_required, current_user
from datetime import datetime
from .models import Task, Forum  # Import Task model
from . import db
import json

# Defining multiple views
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        if 'forum' in request.form:
            forum_data = request.form.get('forum')

            if len(forum_data) < 1:
                flash('Forum is too short!', category='error')
            else:
                new_forum = Forum(Post=forum_data, date=datetime.now(), user_id=current_user.id)
                db.session.add(new_forum)
                db.session.commit()
                flash('Forum added!', category='success')
        elif 'title' in request.form:  # Check if task form is submitted
            title = request.form.get('title')
            people_assigned = request.form.get('people_assigned')
            due_date = datetime.strptime(request.form.get('due_date'), '%Y-%m-%d')
            description = request.form.get('description')
            difficulty = request.form.get('difficulty')

            new_task = Task(title=title, people_assigned=people_assigned, due_date=due_date,
                            description=description, difficulty=difficulty, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash('Task added!', category='success')

    all_forum_posts = Forum.query.all()
    all_tasks = Task.query.all()

    return render_template("home.html", user=current_user, forum_posts=all_forum_posts, tasks=all_tasks)


@views.route('/delete-forum', methods=['POST'])
def delete_forum():
    forum = json.loads(request.data)
    forumID = forum['forumID']
    forum = Forum.query.get(forumID)
    if forum:
        if forum.user_id == current_user.id:
            db.session.delete(forum)
            db.session.commit()

    return jsonify(success=True)  # You can send a response to indicate successful deletion


@views.route('/delete-task', methods=['POST'])
def delete_task():
    task = json.loads(request.data)
    taskID = task['taskID']
    task = Task.query.get(taskID)
    if task:
        if task.user_id == current_user.id:
            db.session.delete(task)
            db.session.commit()

    return jsonify(success=True)  # You can send a response to indicate successful deletion
