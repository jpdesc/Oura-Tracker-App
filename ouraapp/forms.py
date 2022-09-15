from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, FileField, SelectField, DateField, FloatField, IntegerField, PasswordField, ValidationError
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, InputRequired, Optional, EqualTo
from ouraapp.database import Tag
from wtforms_sqlalchemy.fields import QuerySelectMultipleField


def tag_query():
    return Tag.query.order_by(Tag.tag)


class JournalForm(FlaskForm):
    journal = StringField('Notes:',
                          validators=[DataRequired()],
                          widget=TextArea(),
                          render_kw={
                              'cols': 25,
                              'rows': 4
                          })
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
    new_tags = StringField('Add new tags:',
                           widget=TextArea(),
                           render_kw={
                               'cols': 15,
                               'rows': 1
                           })
    select_tags = QuerySelectMultipleField(query_factory=tag_query)
    submit1 = SubmitField("Submit Wellness")


class WorkoutForm(FlaskForm):
    soreness = RadioField('Soreness:', choices=['1', '2', '3', '4', '5'])
    grade = RadioField('Workout Grade:', choices=['1', '2', '3', '4', '5'])
    type = SelectField(
        choices=['Swim', 'Weights', 'Calisthenics', 'Yoga', 'Other'])
    specify_other = StringField("Specify other: ")
    file = FileField('Upload Workout File:')
    workout_log = StringField('Workout Notes:',
                              widget=TextArea(),
                              render_kw={
                                  'cols': 25,
                                  'rows': 4
                              })
    submit2 = SubmitField("Submit Workout")


class TemplateForm(FlaskForm):
    template_name = StringField('G Sheets Template Name: ')
    total_days = IntegerField('Enter number of unique workouts in template:')
    day_one = IntegerField("Day 1 Row: ")
    one_excs = IntegerField("Day 1 Total Exercises")
    day_two = IntegerField("Day 2 Row: ")
    two_excs = IntegerField("Day 2 Total Exercises")
    day_three = IntegerField("Day 3 Row: ")
    three_excs = IntegerField("Day 3 Total Exercises")
    day_four = IntegerField("Day 4 Row: ")
    four_excs = IntegerField("Day 4 Total Exercises")
    day_five = IntegerField("Day 5 Row: ")
    five_excs = IntegerField("Day 5 Total Exercises")
    day_six = IntegerField("Day 6 Row: ")
    six_excs = IntegerField("Day 6 Total Exercises")
    submit = SubmitField("Submit")


class FilterForm(FlaskForm):
    tag_filter = QuerySelectMultipleField('Tags ', query_factory=tag_query)

    sleep_filter = SelectField('Sleep ',
                               choices=[
                                   '', 'Sleep Score', 'Efficiency Score',
                                   'Food Timing 0-1.5', 'Food Timing 1.5-3',
                                   'Food Timing 3-4.5', 'Food Timing 4.5+'
                               ])
    sleep_operator = SelectField(
        choices=['', '>', '<', 'between'],
        render_kw={'onchange': "secondField('sleep_second')"})
    sleep_first = IntegerField()
    sleep_second = IntegerField(validators=[Optional()])

    readiness_filter = SelectField(
        'Readiness ',
        choices=['', 'Readiness', 'Recovery Index', 'Temperature Score'])
    readiness_operator = SelectField(choices=['', '>', '<', 'between'])
    readiness_first = IntegerField()
    readiness_second = IntegerField(validators=[Optional()])

    wellness_filter = SelectField(
        'Wellness ', choices=['', 'Focus', 'Energy', 'Mood', 'Stress'])
    wellness_operator = SelectField(choices=['', '>', '<', 'between'])
    wellness_first = IntegerField()
    wellness_second = IntegerField(validators=[Optional()])

    workout_filter = SelectField('Workout ', choices=['', 'Grade', 'Soreness'])
    workout_operator = SelectField(choices=['', '>', '<', 'between'])
    workout_first = IntegerField()
    workout_second = IntegerField(validators=[Optional()])
    start_date = DateField('Date Range:', format='%Y-%m-%d')
    end_date = DateField(format='%Y-%m-%d')

    submit = SubmitField("Submit Filters")


class RegistrationForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    password1 = PasswordField('Password',
                              validators=[
                                  DataRequired(),
                                  EqualTo('password2',
                                          message='Passwords Must Match!')
                              ])
    password2 = PasswordField('Confirm Password')
    email = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password')
    submit = SubmitField('Submit')
