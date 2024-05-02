# Init.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Secret Senior Project'

    # Construct absolute path to the database file within the 'website' directory
    DATABASE_PATH = path.join(path.dirname(__file__), 'database.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Forum

    # Create the database tables within the application context
    with app.app_context():
        create_database()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database():
    # Construct absolute path to the database file within the 'website' directory
    DATABASE_PATH = path.join(path.dirname(__file__), 'database.db')

    if not path.exists(DATABASE_PATH):
        db.create_all()
        print('Created Database!')