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
    custom_pr_name = StringField('Exercise Name: ',
                                 render_kw={'style': 'width: 15ch'})
    custom_pr_weight = IntegerField('1 Rep Max: ',
                                    render_kw={'style': 'width: 5ch'})


class InitWorkoutForm(FlaskForm):
    name_workout_plan = StringField('Name of workout plan: ')
    days = IntegerField('# of workouts in template: ')
    bench_pr = IntegerField('Bench Press',
                            validators=[Optional()],
                            render_kw={'style': 'width: 5ch'})
    squat_pr = IntegerField('Back Squat',
                            validators=[Optional()],
                            render_kw={'style': 'width: 5ch'})
    deadlift_pr = IntegerField('Deadlift',
                               validators=[Optional()],
                               render_kw={'style': 'width: 5ch'})
    ohp_pr = IntegerField('Overhead Press',
                          validators=[Optional()],
                          render_kw={'style': 'width: 5ch'})

    custom_prs = FieldList(FormField(CustomPR),
                           min_entries=4,
                           max_entries=8,
                           validators=[Optional()],
                           render_kw={'style': 'width: 5ch'})
    submit = SubmitField("Submit")


class WeightsForm(FlaskForm):
    soreness = RadioField('Soreness:', choices=['1', '2', '3', '4', '5'])
    grade = RadioField('Workout Grade:', choices=['1', '2', '3', '4', '5'])
    notes = TextAreaField('Workout Notes:')
    submit2 = SubmitField("Submit Workout")
