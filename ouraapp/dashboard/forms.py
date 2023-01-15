from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, FileField, SelectField, DateField, FloatField, IntegerField, PasswordField, ValidationError
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, InputRequired
from .models import Tag
from wtforms_sqlalchemy.fields import QuerySelectMultipleField


def tag_query():
    return Tag.query.order_by(Tag.tag)


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
        'Create new:',
        widget=TextArea(),
    )
    select_tags = QuerySelectMultipleField(query_factory=tag_query)
    submit1 = SubmitField("Submit Wellness")


class WorkoutForm(FlaskForm):
    soreness = RadioField('Soreness:', choices=['1', '2', '3', '4', '5'])
    grade = RadioField('Workout Grade:', choices=['1', '2', '3', '4', '5'])
    type = SelectField(
        choices=['Swim', 'Weights', 'Calisthenics', 'Yoga', 'Other'])
    specify_other = StringField("Create new: ")
    file = FileField('Upload Workout File:')
    workout_log = StringField(
        'How was your workout?',
        widget=TextArea(),
    )
    submit2 = SubmitField("Submit Workout")
