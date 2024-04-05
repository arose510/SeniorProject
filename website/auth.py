from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successful!', category='successs')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout Successful.', category='success')
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET','POST'])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        fullname = request.form.get("fullname")
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('User/Email already exists.', category='error')
            return redirect(url_for('auth.signup'))

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(fullname) < 2:
            flash('Fullname must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('Passwords must match.', category='error')
        elif len(password1) < 6:              
            flash('Password must be greater than 5 characters.', category='error')
        else:
            # Generate hashed password using pbkdf2:sha256 method
            hashed_password = generate_password_hash(password1, method='pbkdf2:sha256')

            # Create new user and add to the database
            new_user = User(email=email, full_name=fullname, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            
            # Log in the newly created user
            login_user(new_user, remember=True)

            flash('Account created successfully!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
