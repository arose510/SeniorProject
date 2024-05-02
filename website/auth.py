from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from website.models import User
from . import db
from msal import ConfidentialClientApplication

auth = Blueprint('auth', __name__)

# Azure AD B2C configuration
CLIENT_ID = '0473c1f2-3345-4fcb-bb22-cd99fe3dcc9a'
CLIENT_SECRET = '8749d86f-b2cf-4b0a-9509-255863951121'
AUTHORITY = 'https://RoseteChico.b2clogin.com/RoseteChico.onmicrosoft.com/oauth2/v2.0/'
REDIRECT_PATH = 'https://chicoseniorpro.azurewebsites.net'  # Update this with your actual redirect URL
SCOPE = ["openid", "offline_access", "profile", "email", "User.Read"]

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            flash('Logged in successfully!', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Incorrect email or password.', category='error')

    return render_template("login.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', category='success')
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        email = request.form.get('email')
        full_name = request.form.get('fullname')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if User.query.filter_by(email=email).first():
            flash('Email address already exists.', category='error')
        elif password != confirm_password:
            flash('Passwords do not match.', category='error')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(email=email, full_name=full_name, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created successfully!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")

@auth.route('/getAToken')
def get_token():
    result = _build_msal_app().initiate_auth_code_flow(
        scopes=SCOPE,
        redirect_uri=REDIRECT_PATH)

    return redirect(result['auth_uri'])

@auth.route('/getAToken/redirect')
def get_token_redirect():
    result = _build_msal_app().acquire_token_by_auth_code_flow(request.args)
    if 'error' in result:
        flash('Authentication failed: ' + result['error'], category='error')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=result['id_token_claims']['email']).first()
    if user:
        login_user(user, remember=True)
        flash('Logged in successfully!', category='success')
        return redirect(url_for('views.home'))
    else:
        flash('Email does not exist.', category='error')
        return redirect(url_for('auth.login'))

def _build_msal_app():
    return ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET)
