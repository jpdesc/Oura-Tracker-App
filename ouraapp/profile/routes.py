from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from flask import request, redirect, url_for, render_template
from ouraapp.auth.models import User
from ouraapp.extensions import db
from .forms import EditProfileForm
from ouraapp.profile import bp
from werkzeug.security import generate_password_hash, check_password_hash


@bp.route(f'/profile/<int:edit>', methods=['GET', 'POST'])
@login_required
def profile(edit):
    user = User.query.filter_by(id=current_user.id).first()
    username = user.username
    name = user.name
    password = user.password_hash
    oura_access_token = user.oura_access_token
    join_date = user.join_date
    email = user.email
    form = EditProfileForm(username=username,
                           email=email,
                           name=name,
                           oura_access_token=oura_access_token)

    if form.validate_on_submit():
        user.username = form.username.data
        user.name = form.name.data
        user.email = form.email.data
        if form.password1.data:
            user.password = form.password1.data
        user.oura_access_token = form.oura_access_token.data
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('profile', edit=0))

    return render_template('profile.html',
                           form=form,
                           username=username,
                           name=name,
                           oura_access_token=oura_access_token,
                           join_date=join_date,
                           edit=edit,
                           password=password,
                           email=email)
