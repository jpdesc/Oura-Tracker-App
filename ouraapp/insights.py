from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from ouraapp.database import Tag, Sleep, Readiness, Log, Workout, db, tags
from datetime import date
from sqlalchemy import and_, func, cast, Numeric

db_fields = {
    'sleep_score': Sleep.sleep_score,
    'rem_score': Sleep.rem_score,
    'deep_score': Sleep.deep_score,
    'seconds_sleep': Sleep.seconds_sleep,
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
    'avg_total_sleep': ('seconds_sleep', Sleep),
    'avg_sleep_score': ('sleep_score', Sleep),
    'avg_rem_score': ('rem_score', Sleep),
    'avg_deep_score': ('deep_score', Sleep),
    'avg_sleep_efficiency': ('sleep_efficiency', Sleep),
    'avg_readiness_score': ('readiness_score', Readiness),
    'avg_recovery_index': ('recovery_index', Readiness),
    'avg_hrv_balance': ('hrv_balance', Readiness),
    'avg_food_cutoff': ('food_cutoff', Sleep)
}


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
    second_conditions = []
    for tag in selected_tags:
        conditions.append(Log.tags.any(Tag.tag == tag))
    conditions.append(Log.date >= date_range[0])
    conditions.append(Log.date <= date_range[1])
    for statement in format_filters(form):
        second_conditions.append(statement)
    condition = and_(*conditions)
    second_condition = and_(*second_conditions)
    filter_result = Log.query.join(
        Log.tags).filter(condition).filter(second_condition).all()
    return filter_result


def get_filtered_avgs(filtered_objs):
    filter_avgs = {}
    id_nums = [log.id + 1 for log in filtered_objs]
    for key, value in avg_fields.items():
        db_attr = db_fields[value[0]]
        attr = value[0]
        db_class = value[1]
        id_attr = db_class.id
        db_objs = db_class.query.filter(id_attr.in_(id_nums)).order_by(id_attr)
        subquery = db_objs.with_entities(db_attr).subquery()
        subquery_c = getattr(subquery.c, attr)
        if key == 'avg_food_cutoff':
            filter_avgs[key] = db.session.query(
                func.round(func.avg(subquery_c).cast(Numeric), 1)).scalar()
            print(filter_avgs[key])
        elif key == 'avg_total_sleep':
            filter_avgs[key] = convert_seconds(
                db.session.query(func.avg(subquery_c)).scalar())
        else:
            filter_avgs[key] = db.session.query(
                func.round(func.avg(subquery_c), 1)).scalar()
    return filter_avgs


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
        'Sleep Score': (Sleep.sleep_score, Sleep.id),
        'Efficiency Score': (Sleep.sleep_efficiency, Sleep.id),
        'Readiness': (Readiness.readiness_score, Readiness.id),
        'Recovery Index': (Readiness.recovery_index, Readiness.id),
        'Temperature Score': (Readiness.temperature, Readiness.id),
        'Focus': (Log.focus, Log.id),
        'Energy': (Log.energy, Log.id),
        'Mood': (Log.mood, Log.id),
        'Stress': (Log.stress, Log.id),
        'Grade': (Workout.grade, Workout.id),
        'Soreness': (Workout.soreness, Workout.id)
    }
    filters = []
    for key, val in filter_fields.items():
        if val[0] != '':
            db_attr = form_db_dict[val[0]][0]
            id_num = form_db_dict[val[0]][1]
            if val[1] == 'between':
                query = db_attr > val[2], db_attr < val[3]
            elif val[1] == '>':
                print('logic working correctly.')
                query = db_attr > val[2]
            elif val[1] == '<':
                query = db_attr < val[2]
            else:
                query = None
            id_check = id_num == Log.id
            filters.append(query)
            filters.append(id_check)
    return filters


def convert_seconds(seconds):
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    return "%d:%02d" % (hour, minutes)


def get_overall_averages():
    averages = {}
    for key, value in avg_fields.items():
        db_attr = db_fields[value[0]]
        if key == 'avg_food_cutoff':
            averages[key] = db.session.query(
                func.round(func.avg(db_attr).cast(Numeric), 1)).scalar()
        elif key == 'avg_total_sleep':
            averages[key] = convert_seconds(
                db.session.query(func.avg((db_attr))).scalar())
        else:
            averages[key] = db.session.query(
                db.func.round(func.avg(db_attr), 1)).scalar()
    return averages
