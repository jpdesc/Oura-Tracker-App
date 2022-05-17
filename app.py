from io import BytesIO
import os
from flask import render_template, session, redirect, url_for, request, send_file
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, FileField, SelectField, BooleanField, FloatField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, InputRequired
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from datetime import date, timedelta
from fetch_oura_data import setup_oura_data, today, date_str_cal, id_dict
from weights_data import get_weights_data
from database import db, Sleep, Log, Tag, Readiness, Workout, Weights, app
from insights import FilterForm, get_overall_averages, get_filters, get_date_range

basedir = os.path.abspath(os.path.dirname(__file__))
bootstrap = Bootstrap(app)


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
    food_cutoff = FloatField('How many hours before bed was your last meal?',
                             validators=[InputRequired()])
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
    type = SelectField(choices=['Swim', 'Weights', 'Other'])
    specify_other = StringField("Specify other: ")
    file = FileField('Upload Workout File:')
    workout_log = StringField('Workout Notes:',
                              widget=TextArea(),
                              render_kw={
                                  'cols': 25,
                                  'rows': 4
                              })
    submit2 = SubmitField("Submit Workout")


events = []


def get_date(page_id, id_dict):
    for key, value in id_dict.items():
        if value == page_id:
            return key


def create_cal_events():
    sleep_query = Sleep.query.order_by(Sleep.id).all()
    for sleep in sleep_query:
        events.append({'title': 'Sleep', 'date': sleep.date, 'id': sleep.id})

    log_query = Log.query.order_by(Log.id).all()
    for log in log_query:
        events.append({
            'title': 'Wellness Log',
            'date': log.date,
            'id': log.id
        })

    workout_query = Workout.query.order_by(Workout.id).all()
    for workout in workout_query:
        events.append({
            'title': workout.type,
            'date': workout.date,
            'id': workout.id
        })


def update_log_events(submitted_log):
    events.append({
        'title': 'Wellness Log',
        'date': submitted_log.date,
        'id': submitted_log.id
    })


def update_workout_events(submitted_log, type):
    events.append({
        'title': type,
        'date': submitted_log.date,
        'id': submitted_log.id
    })


def get_workout_week_num():
    last_workout = Weights.query.order_by(Weights.id.desc()).first()
    if last_workout.workout_id == 4:
        week = last_workout.workout_week + 1
    else:
        week = last_workout.workout_week
    return week


def get_workout_id():
    last_workout = Weights.query.order_by(Weights.id.desc()).first()
    if last_workout.workout_id == 4:
        workout_id = 1
    else:
        workout_id = last_workout.workout_id + 1
    return workout_id


def check_improvement(this_week, last_week):
    reps_improvement, weight_improvement = [], []
    for i, exercise in enumerate(this_week.exercises):
        reps_check = False
        weight_check = False
        try:
            check_empty_reps = (this_week.reps[i] and last_week.reps[i]) != ''
            check_empty_weight = (this_week.reps[i]
                                  and last_week.reps[i]) != ''
            exercises_match = exercise == last_week.exercises[i]
        except IndexError:
            reps_improvement.append(False)
            weight_improvement.append(False)
            continue
        if exercises_match and check_empty_reps:
            try:
                reps_check = int(this_week.reps[i]) > int(last_week.reps[i]) \
                  and int(this_week.weight[i]) >= int(last_week.weight[i])
            except ValueError:
                reps_check = False
        if exercises_match and check_empty_weight:
            try:
                weight_check = float(this_week.weight[i]) > float(
                    last_week.weight[i])
            except ValueError:
                weight_check = False
        reps_improvement.append(reps_check)
        weight_improvement.append(weight_check)
    return reps_improvement, weight_improvement


def get_tags(added_tags, selected_tags):
    tags = []
    if added_tags:
        for word in added_tags.split(','):
            stripped = word.strip(', ').lower()
            tags.append(stripped)
    if selected_tags:
        for tag in selected_tags:
            if tag not in tags:
                tags.append(tag)
    return tags


def add_tags(added_tags, selected_tags, db_obj):
    for entry in get_tags(added_tags, selected_tags):
        existing_entry = Tag.query.filter(Tag.tag == str(entry)).first()
        if existing_entry:
            tag_obj = existing_entry
        else:
            tag_obj = Tag(tag=str(entry))
        db_obj.tags.append(tag_obj)


def create_id_dict():
    all_days = [
        date(2022, 1, 1) + timedelta(days=x)
        for x in range((today - date(2022, 1, 1)).days + 5)
    ]
    for i, day in enumerate(all_days):
        id_dict[day] = i
        date_str_cal[str(day)] = id_dict[day]


@app.route('/', defaults={'page_id': id_dict[today]}, methods=['GET', 'POST'])
@app.route('/<int:page_id>', methods=['GET', 'POST'])
def index(page_id):
    date = get_date(page_id, id_dict)
    wellness_form = JournalForm()
    workout_form = WorkoutForm()
    sleep = Sleep.query.filter(Sleep.id == page_id).first()
    log = Log.query.filter(Log.id == page_id).first()
    readiness = Readiness.query.filter(Readiness.id == page_id).first()
    workout = Workout.query.filter(Workout.id == page_id).first()

    if wellness_form.validate_on_submit():
        journal = wellness_form.journal.data
        focus = wellness_form.focus.data
        mood = wellness_form.mood.data
        energy = wellness_form.energy.data
        stress = wellness_form.stress.data
        added_tags = wellness_form.new_tags.data
        selected_tags = wellness_form.select_tags.data
        wellness_info = Log(journal=journal,
                            focus=focus,
                            mood=mood,
                            energy=energy,
                            date=date,
                            id=page_id,
                            stress=stress)
        if selected_tags or added_tags:
            add_tags(added_tags, selected_tags, wellness_info)
        db.session.add(wellness_info)
        db.session.commit()
        update_log_events(wellness_info)
        if sleep:
            sleep.food_cutoff = wellness_form.food_cutoff.data
            db.session.add(sleep)
            db.session.commit()
        return redirect(url_for('index', page_id=page_id))

    if workout_form.validate_on_submit():
        file = request.files[str(workout_form.file.name)]
        type = workout_form.type.data
        if type == "Other":
            type = workout_form.specify_other.data
        soreness = workout_form.soreness.data
        grade = workout_form.grade.data
        workout_log = workout_form.workout_log.data
        workout_info = Workout(data=file.read(),
                               date=date,
                               id=page_id,
                               filename=file.filename,
                               type=type,
                               soreness=soreness,
                               grade=grade,
                               workout_log=workout_log)
        if type == "Weights":
            get_weights_data(get_workout_id(), get_workout_week_num(), page_id)
        db.session.add(workout_info)
        db.session.commit()
        update_workout_events(workout_info, type)
        return redirect(url_for('index', page_id=page_id))

    return render_template('index.html',
                           wellness_form=wellness_form,
                           workout_form=workout_form,
                           sleep=sleep,
                           log=log,
                           page_id=page_id,
                           date=date,
                           readiness=readiness,
                           workout=workout)


@app.route('/edit/<int:page_id>', methods=['GET', 'POST'])
def edit_log(page_id):
    date = get_date(page_id, id_dict)
    sleep = Sleep.query.get(page_id)
    readiness = Readiness.query.get(page_id)
    log = Log.query.get(page_id)
    workout = Workout.query.get(page_id)
    if log:
        wellness_form = JournalForm(focus=log.focus,
                                    mood=log.mood,
                                    energy=log.energy,
                                    stress=log.stress,
                                    journal=log.journal,
                                    select_tags=log.tags)
    else:
        wellness_form = JournalForm()
    if workout:
        workout_form = WorkoutForm(soreness=workout.soreness,
                                   type=workout.type,
                                   specify_other=None,
                                   file=workout.data,
                                   grade=workout.grade,
                                   workout_log=workout.workout_log)
    else:
        workout_form = WorkoutForm()
    if wellness_form.validate_on_submit():
        log.focus = wellness_form.focus.data
        log.mood = wellness_form.mood.data
        log.energy = wellness_form.energy.data
        log.journal = wellness_form.journal.data
        log.stress = wellness_form.stress.data
        log.tags = wellness_form.select_tags.data
        added_tags = wellness_form.new_tags.data
        selected_tags = None
        if added_tags:
            add_tags(added_tags, selected_tags, log)
        db.session.add(log)
        db.session.commit()
        if sleep:
            sleep.food_cutoff = wellness_form.food_cutoff.data
            db.session.add(sleep)
            db.session.commit()
        return redirect(url_for('index', page_id=page_id))

    if workout_form.validate_on_submit():
        workout.soreness = workout_form.soreness.data
        workout.grade = workout_form.grade.data
        workout.workout_log = workout_form.workout_log.data
        if workout.type == 'Other':
            workout.type = workout_form.specify_other.data
        else:
            workout.type = workout_form.type.data
            workout.file = workout_form.file.data
        db.session.add(workout)
        db.session.commit()
        return redirect(url_for('index', page_id=page_id))
    return render_template('edit_post.html',
                           wellness_form=wellness_form,
                           workout_form=workout_form,
                           sleep=sleep,
                           page_id=page_id,
                           readiness=readiness,
                           date=date)


@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    session['url'] = url_for('index', page_id=None)
    return render_template('calendar.html', events=events)


@app.route('/process', methods=['POST'])
def process():
    ''' Used to process ajax call for calendar event clicks.
  Routes to the correct index page based on the page_id/dates.
  '''
    date_str = request.form.get('date_str')
    clicked_id = date_str_cal[date_str]
    return redirect(url_for('index', page_id=clicked_id))


@app.route('/download/<page_id>')
def download(page_id):
    workout = Workout.query.filter_by(id=page_id).first()
    return send_file(BytesIO(workout.data),
                     attachment_filename=workout.filename,
                     as_attachment=True)


@app.route('/weights/<page_id>')
def weights(page_id):
    this_week = Weights.query.filter_by(id=page_id).first()
    try:
        last_week = Weights.query.filter_by(
            workout_id=this_week.workout_id,
            workout_week=(this_week.workout_week - 1)).first()
        reps_improve, weight_improve = check_improvement(this_week, last_week)
    except (AttributeError):
        reps_improve, weight_improve = None, None
    return render_template('workout.html',
                           page_id=page_id,
                           weights=this_week,
                           reps_improve=reps_improve,
                           weight_improve=weight_improve)


@app.route('/insights', methods=['GET', 'POST'])
def insights():
    filter_form = FilterForm()
    averages = get_overall_averages()
    if request.method == "POST":
        date_range = get_date_range(filter_form)
        get_filters(filter_form, date_range)
        return redirect(url_for('insights'))

    return render_template('insights.html',
                           averages=averages,
                           filter_form=filter_form)


if __name__ == '__main__':
    setup_oura_data()
    create_cal_events()
    app.run(debug=True)
