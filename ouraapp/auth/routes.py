from flask import render_template, redirect, url_for, flash, Blueprint
from .helpers import setup_oura_data
from ouraapp.auth.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import LoginForm, RegistrationForm
from flask_login import login_user, login_required, logout_user, current_user
from ouraapp.extensions import db, login_manager
import logging
from ouraapp.auth import bp

logger = logging.getLogger("ouraapp")


@login_manager.user_loader
def load_user(user_id):
    '''Check if user is logged in on every page load.'''
    if user_id is not None:
        return User.query.get(int(user_id))
    print('user_id is None')
    return None


@login_manager.unauthorized_handler
def unauthorized():
    '''Redirect unauthorized users to Login page.'''
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth.login'))


@bp.route('/auth/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.log'))
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        existing_user = User.query.filter_by(
            email=registration_form.email.data).first()
        if existing_user is None:
            hashed_password = generate_password_hash(
                registration_form.password1.data, "sha256")
            user = User(username=registration_form.username.data,
                        name=registration_form.name.data,
                        password_hash=hashed_password,
                        email=registration_form.email.data)
            flash('Welcome, {username}. You are now a registered user!')
            db.session.add(user)
            db.session.commit()
            login_user(user)
            setup_oura_data()
            return redirect(url_for('dashboard.log'))
        flash('A user already exists with that email address.')

    return render_template('registration.html', form=registration_form)


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/auth/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.log'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = User.query.filter_by(username=username).first()
        if user:
            passed = check_password_hash(user.password_hash, password)
            if passed:
                login_user(user)
                # create_all_cal_events()
                setup_oura_data()
                return redirect(url_for('dashboard.log'))
            else:
                flash("Wrong password - try again.")
        else:
            flash("That user doesn't exist - try again...")
    return render_template('index.html', login_form=login_form)


@bp.route('/auth/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out.")
    return redirect(url_for('auth.login'))
