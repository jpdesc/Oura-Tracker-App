from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DateField, IntegerField
from wtforms.validators import Optional
from ouraapp.dashboard.models import Tag
from wtforms_sqlalchemy.fields import QuerySelectMultipleField


def tag_query():
    return Tag.query.order_by(Tag.tag)


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
