from flask import Blueprint, jsonify, render_template, request, flash
from flask_login import login_required, current_user
from datetime import datetime  # Import datetime
from .models import Forum
from . import db
import json

# Defining multiple views
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        forum_data = request.form.get('forum')

        if len(forum_data) < 1:
            flash('Forum is too short!', category='error')
        else:
            # Use func.now() to get the current timestamp
            new_forum = Forum(Post=forum_data, date=datetime.now(), user_id=current_user.id)
            db.session.add(new_forum)
            db.session.commit()
            flash('Forum added!', category='success')

    # Get all forum posts from the database
    all_forum_posts = Forum.query.all()

    return render_template("home.html", user=current_user, forum_posts=all_forum_posts)

@views.route('/delete-forum', methods=['POST'])
def delete_forum():
    forum = json.loads(request.data)
    forumID = forum['forumID'] 
    forum = Forum.query.get(forumID)
    if forum:
        if forum.user_id == current_user.id:
            db.session.delete(forum)
            db.session.commit()

    return jsonify({})