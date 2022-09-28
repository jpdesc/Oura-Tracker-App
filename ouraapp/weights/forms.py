from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FieldList, FormField, BooleanField


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
    excs = IntegerField('Exercise Name: ')
    sets = IntegerField('Sets: ')
    reps1 = IntegerField('Rep range: ')
    reps2 = IntegerField()


class WorkoutForm(FlaskForm):
    exercise_params = FieldList(FormField(TemplateForm2),
                                min_entries=10,
                                max_entries=15)
    submit = SubmitField("Submit")


class CustomPR(FlaskForm):
    custom_pr_name = StringField('Exercise Name: ')
    custom_pr_weight = IntegerField('1 Rep Max: ')


class InitWorkoutForm(FlaskForm):
    name_workout_plan = StringField('Name of workout plan: ')
    set_base = BooleanField('Create a base template for your workouts?')
    days = IntegerField('Enter the number of workouts per weekly cycle: ')
    set_pr = BooleanField('Enter one rep maxes at start of program?')
    bench_pr = IntegerField('Bench 1 Rep Max: ')
    squat_pr = IntegerField('Back Squat 1 Rep Max: ')
    deadlift_pr = IntegerField('Deadlift 1 Rep Max: ')
    ohp_pr = IntegerField('Overhead Press 1 Rep Max: ')
    custom_pr = BooleanField('Record additional PRs? ')
    custom_prs = FieldList(FormField(CustomPR), min_entries=1, max_entries=5)
    submit = SubmitField("Submit")
