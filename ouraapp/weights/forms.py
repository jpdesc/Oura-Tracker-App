from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField


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
