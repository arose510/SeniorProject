from flask_login import UserMixin
from datetime import datetime
from . import db

class Task(db.Model):
    """Class representing a Task"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    people_assigned = db.Column(db.String(200))  # You can adjust the length as needed
    due_date = db.Column(db.DateTime(timezone=True))
    description = db.Column(db.String(500))
    difficulty = db.Column(db.Enum('Easy', 'Medium', 'Hard'))  # Adjust difficulty levels as needed
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='tasks')

class Forum(db.Model):
    """Class representing a Forum Post"""
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(5000))
    date = db.Column(db.DateTime(timezone=True), default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    """Class representing a User"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(100))
    full_name = db.Column(db.String(150))
    forum = db.relationship('Forum', backref='user')
    tasks = db.relationship('Task', back_populates='user')