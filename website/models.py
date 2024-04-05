"""Module providing user-related functionality and database models."""
from flask_login import UserMixin
from sqlalchemy.sql import func

from . import db

class Forum(db.Model):
    """Class representing a Forum Post"""
    id = db.Column(db.Integer, primary_key=True)
    Post = db.Column(db.String(5000))
    date = db.Column(db.DateTime(timezone=True), default = func.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#User Class Initialization
class User(db.Model, UserMixin):
    """Class representing a User"""
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(100))
    full_name = db.Column(db.String(150))
    forum = db.relationship('Forum')
