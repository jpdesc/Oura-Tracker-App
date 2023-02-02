from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, FileField, SelectField, DateField, FloatField, IntegerField, PasswordField, ValidationError
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, InputRequired
from .models import Tag
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from flask_login import current_user
import logging

logger = logging.getLogger("ouraapp")


def tag_query():
    logger.debug(f'tag_query test: {Tag.query.order_by(Tag.tag).filter(Tag.user_id == current_user.id)}')
    return Tag.query.order_by(Tag.tag).filter(Tag.user_id == current_user.id)


class JournalForm(FlaskForm):
    journal = StringField(
        'How are you feeling?',
        validators=[DataRequired()],
        widget=TextArea(),
    )
    focus = RadioField('Focus: ',
                       choices=['1', '2', '3', '4', '5'],
                       validators=[InputRequired()])
    mood = RadioField('Mood: ',
                      choices=['1', '2', '3', '4', '5'],
                      validators=[InputRequired()])
    energy = RadioField('Energy: ',
                        choices=['1', '2', '3', '4', '5'],
                        validators=[InputRequired()])
    stress = RadioField('Stress: ',
                        choices=['1', '2', '3', '4', '5'],
                        validators=[InputRequired()])
    food_cutoff = FloatField('How many hours before bed was your last meal?')
    new_tags = StringField(
        'New Type',
        # widget=TextArea(),
    )
    select_tags = QuerySelectMultipleField(query_factory=tag_query)
    submit1 = SubmitField("")


class WorkoutForm(FlaskForm):
    soreness = RadioField('Soreness:', choices=['1', '2', '3', '4', '5'])
    grade = RadioField('Intensity:', choices=['1', '2', '3', '4', '5'])
    type = SelectField(
        choices=['Swim', 'Weights', 'Calisthenics', 'Yoga', 'Other'])
    specify_other = StringField("New Type: ")
    file = FileField('Upload Workout File:')
    workout_log = StringField(
        'How was your workout?',
        widget=TextArea(),
    )
    submit2 = SubmitField("")
