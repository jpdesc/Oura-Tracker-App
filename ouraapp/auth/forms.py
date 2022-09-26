from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Email
from .models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password1 = PasswordField('Password',
                              validators=[
                                  DataRequired(),
                                  EqualTo('password2',
                                          message='Passwords Must Match!')
                              ])
    password2 = PasswordField('Confirm Password')
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user is not None:
        raise ValidationError('Please use a different username.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password')
    submit = SubmitField('Submit')
