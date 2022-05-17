from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, BooleanField, FloatField, IntegerField, DateField
from wtforms.validators import DataRequired, InputRequired, Optional
from yaml import TagToken
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from database import Tag, Sleep, Readiness, Log, Workout, db, tags
from datetime import date
from sqlalchemy import and_

db_fields = {
    'sleep_score': Sleep.sleep_score,
    'rem_score': Sleep.rem_score,
    'deep_score': Sleep.deep_score,
    'total_sleep': Sleep.seconds_sleep,
    'total_rem_sleep': Sleep.total_rem_sleep,
    'total_deep_sleep': Sleep.total_deep_sleep,
    'food_cutoff': Sleep.food_cutoff,
    'restlessness': Sleep.restlessness,
    'sleep_efficiency': Sleep.sleep_efficiency,
    'readiness_score': Readiness.readiness_score,
    'recovery_index': Readiness.recovery_index,
    'resting_hr': Readiness.resting_hr,
    'temperature': Readiness.temperature,
    'hrv_balance': Readiness.hrv_balance,
    'soreness': Workout.soreness,
    'grade': Workout.grade,
    'type': Workout.type,
    'focus': Log.focus,
    'mood': Log.mood,
    'energy': Log.energy,
    'stress': Log.stress
}

avg_fields = {
    'avg_total_sleep': 'total_sleep',
    'avg_sleep_score': 'sleep_score',
    'avg_rem_score': 'rem_score',
    'avg_deep_score': 'deep_score',
    'avg_sleep_efficiency': 'sleep_efficiency',
    'avg_readiness_score': 'readiness_score',
    'avg_recovery_index': 'recovery_index',
    'avg_hrv_balance': 'hrv_balance',
    'avg_food_cutoff': 'food_cutoff'
}


def tag_query():
    return Tag.query.order_by(Tag.tag)


class FilterForm(FlaskForm):
    tag_filter = QuerySelectMultipleField('Tag Filters',
                                          query_factory=tag_query)
    sleep_filter = SelectField('Sleep Filters',
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
        'Readiness Filters',
        choices=['', 'Readiness', 'Recovery Index', 'Temperature Score'])
    readiness_operator = SelectField(choices=['', '>', '<', 'between'])
    readiness_first = IntegerField()
    readiness_second = IntegerField(validators=[Optional()])

    wellness_filter = SelectField(
        'Wellness Filters', choices=['', 'Focus', 'Energy', 'Mood', 'Stress'])
    wellness_operator = SelectField(choices=['', '>', '<', 'between'])
    wellness_first = IntegerField()
    wellness_second = IntegerField(validators=[Optional()])

    workout_filter = SelectField('Workout Filters',
                                 choices=['', 'Grade', 'Soreness'])
    workout_operator = SelectField(choices=['', '>', '<', 'between'])
    workout_first = IntegerField()
    workout_second = IntegerField(validators=[Optional()])
    start_date = DateField('Date Range:', format='%Y-%m-%d')
    end_date = DateField(format='%Y-%m-%d')

    submit = SubmitField("Submit Filters")


def get_date_range(form):
    date_range = []
    if form.start_date.data:
        start_date = form.start_date.data
    else:
        start_date = date(2022, 1, 1)
    date_range.append(start_date)
    if form.end_date.data:
        end_date = form.end_date.data
    else:
        end_date = date.today()
    date_range.append(end_date)
    return date_range


def get_filters(form, date_range):
    selected_tags = []
    for selected in form.tag_filter.data:
        selected_tags.append(str(selected))
    conditions = []
    for tag in selected_tags:
        conditions.append(Log.tags.any(Tag.tag == tag))
    conditions.append(Log.date >= date_range[0])
    conditions.append(Log.date <= date_range[1])
    for statement in format_filters(form):
        conditions.append(statement)
    condition = and_(*conditions)
    # print(f'condition: {condition}')
    filter_result = Log.query.join(Log.tags).filter(condition).all()
    # print(f'queried {filter_result}')
    return filter_result


def format_filters(form):
    filter_fields = {
        'sleep': [
            form.sleep_filter.data, form.sleep_operator.data,
            form.sleep_first.data, form.sleep_second.data
        ],
        'readiness': [
            form.readiness_filter.data, form.readiness_operator.data,
            form.readiness_first.data, form.readiness_second.data
        ],
        'wellness': [
            form.wellness_filter.data, form.wellness_operator.data,
            form.wellness_first.data, form.wellness_second.data
        ],
        'workout': [
            form.workout_filter.data, form.workout_operator.data,
            form.workout_first.data, form.workout_second.data
        ]
    }
    form_db_dict = {
        'Sleep Score': Sleep.sleep_score,
        'Efficiency Score': Sleep.sleep_efficiency,
        'Readiness': Readiness.readiness_score,
        'Recovery Index': Readiness.recovery_index,
        'Temperature Score': Readiness.temperature,
        'Focus': Log.focus,
        'Energy': Log.energy,
        'Mood': Log.mood,
        'Stress': Log.stress,
        'Grade': Workout.grade,
        'Soreness': Workout.soreness
    }
    filters = []
    for key, val in filter_fields.items():
        if val[0] != '':
            db_attr = form_db_dict[val[0]]
            if val[1] == 'between':
                query = db_attr > val[2], db_attr < val[3]
            elif val[1] == '>':
                print('logic working correctly.')
                query = db_attr > val[2]
            elif val[1] == '<':
                query = db_attr < val[2]
            else:
                query = None
            filters.append(query)
    print(filters[0])
    return filters


def convert_seconds(seconds):
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    return "%d:%02d" % (hour, minutes)


def get_db_objs(date_range):
    sleep_objs = []
    readiness_objs = []
    workout_objs = []
    log_objs = []
    sleep = Sleep.query.filter_by(Sleep.date >= f'{date_range[0]}',
                                  Sleep.date <= f'{date_range[1]}')
    sleep_objs.append(sleep)
    readiness = Readiness.query.filter_by(Readiness.date >= f'{date_range[0]}',
                                          Readiness.date <= f'{date_range[1]}')
    readiness_objs.append(readiness)
    workout = Sleep.query.filter_by(Workout.date >= f'{date_range[0]}',
                                    Workout.date <= f'{date_range[1]}')
    workout_objs.append(workout)
    log = Sleep.query.filter_by(Log.date >= f'{date_range[0]}',
                                Log.date <= f'{date_range[1]}')
    log_objs.append(log)
    return sleep_objs, readiness_objs, workout_objs, log_objs


def get_overall_averages():
    averages = {}
    for key, value in avg_fields.items():
        db_attr = db_fields[value]
        if key == 'avg_food_cutoff':
            averages[key] = db.session.query(db.func.avg(db_attr)).scalar()
        elif key == 'avg_total_sleep':
            averages[key] = convert_seconds(
                db.session.query(db.func.avg((db_attr))).scalar())
        else:
            averages[key] = db.session.query(
                db.func.round(db.func.avg(db_attr), 1)).scalar()
    return averages


# def get_filtered_averages(filters_list, date_range):

# def compare_averages():
#     pass
