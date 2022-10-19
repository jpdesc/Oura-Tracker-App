from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, Optional


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password1 = PasswordField(
        'New Password (Optional)',
        validators=[EqualTo('password2', message='Passwords Must Match!')])
    password2 = PasswordField('Confirm New Password')
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired()])
    oura_access_token = StringField('Oura Access Token',
                                    validators=[Optional()])
    submit = SubmitField('Submit')
