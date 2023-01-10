from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FieldList, FormField, BooleanField, RadioField, TextAreaField
from wtforms.validators import Optional, InputRequired, NumberRange
from wtforms.widgets import TextArea


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


class TemplateForm2(FlaskForm):
    excs = StringField('Exercise Name: ', validators=[Optional()])
    sets = IntegerField('Sets: ',
                        validators=[Optional()],
                        render_kw={'style': 'width: 5ch'})
    reps1 = IntegerField('Rep range: ',
                         validators=[Optional()],
                         render_kw={'style': 'width: 5ch'})
    reps2 = IntegerField(validators=[Optional()],
                         render_kw={'style': 'width: 5ch'})


class WorkoutForm(FlaskForm):
    exercise_params = FieldList(FormField(TemplateForm2),
                                min_entries=10,
                                max_entries=15,
                                validators=[Optional()])
    submit = SubmitField("Submit")


class CustomPR(FlaskForm):
    custom_pr_name = StringField('Exercise Name: ')
    custom_pr_weight = IntegerField('1 Rep Max: ')


class InitWorkoutForm(FlaskForm):
    name_workout_plan = StringField('Name of workout plan: ',
                                    validators=[InputRequired()])
    set_base = BooleanField('Create a base template for your workouts?',
                            render_kw={'onchange': "showFields()"})
    days = IntegerField('Enter the number of workouts per weekly cycle: ',
                        validators=[Optional(),
                                    NumberRange(min=1, max=7)])
    set_pr = BooleanField('Enter one rep maxes at start of program?',
                          validators=[Optional()],
                          render_kw={'onchange': "showFields()"})
    bench_pr = IntegerField('Bench 1 Rep Max: ', validators=[Optional()])
    squat_pr = IntegerField('Back Squat 1 Rep Max: ', validators=[Optional()])
    deadlift_pr = IntegerField('Deadlift 1 Rep Max: ', validators=[Optional()])
    ohp_pr = IntegerField('Overhead Press 1 Rep Max: ',
                          validators=[Optional()])
    custom_pr = BooleanField('Record additional PRs? ',
                             validators=[Optional()],
                             render_kw={'onchange': "showFields()"})
    custom_prs = FieldList(FormField(CustomPR),
                           min_entries=1,
                           max_entries=5,
                           validators=[Optional()])
    submit = SubmitField("Submit")


class WeightsForm(FlaskForm):
    soreness = RadioField('Soreness:', choices=['1', '2', '3', '4', '5'])
    grade = RadioField('Workout Grade:', choices=['1', '2', '3', '4', '5'])
    notes = TextAreaField('Workout Notes:')
    submit2 = SubmitField("Submit Workout")
