from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from flask import request, redirect, url_for, render_template
from ouraapp.auth.models import User
from ouraapp.extensions import db
from ouraapp.auth.forms import RegistrationForm
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
    hashed_password = generate_password_hash(registration_form.password1.data,
                                             "sha256")
    form = RegistrationForm(username=username,
                            password1=password,
                            password2=password,
                            oura_access_token=oura_access_token)

    if request.method == 'Post':
        user.username = form.username.data
        user.name = form.name.data
        user.email = form.email.data
        user.password_hash = generate_password_hash(form.password1.data,
                                                    "sha256")
        user.oura_access_token = form.oura_access_token.data
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('profile'))

    return render_template('profile.html',
                           form=form,
                           username=username,
                           name=name,
                           oura_access_token=oura_access_token,
                           join_date=join_date,
                           edit=edit,
                           password=password)
