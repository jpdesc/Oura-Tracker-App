from io import BytesIO
from venv import create
from flask import render_template, session, redirect, url_for, request, send_file, flash
from datetime import date, timedelta
import json
from ouraapp.fetch_oura_data import setup_oura_data
from ouraapp.weights_data import get_weights_data, get_current_template
from ouraapp.database import Sleep, Log, Tag, Readiness, Workout, Weights, Template, User, Events, Day
from ouraapp.insights import get_overall_averages, get_filters, get_date_range, get_filtered_avgs
from ouraapp.fetch_oura_data import add_event_to_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from ouraapp.forms import *
from ouraapp import db
from ouraapp import login_manager
from run import app


def get_page_id():
    with app.app_context():
        today = date.today()
        db_obj = Day.query.filter_by(date=today).first()
    return db_obj.id


def get_date(page_id):
    db_obj = Day.query.filter_by(id=page_id).first()
    return db_obj.date


def format_date(date):
    '''Format date for display on wellness dashboard.'''
    return date.strftime("%A, %B %-dth")


def get_wellness_score(log):
    if log.stress:
        return (log.focus + log.mood + log.energy + (6 - log.stress)) / 4
    else:
        return None


def str_fmt_date(date_obj):
    return date_obj.strftime('%Y-%m-%d')


def get_db_events():
    '''Format events for use in the calendar.'''
    events = []
    events_objs = Events.query.filter(
        Events.user_id == current_user.id).order_by(Events.id).all()
    for event in events_objs:
        json_event = event.event
        event_dict = json.loads(json_event)
        events.append(event_dict)
    return events


def add_event_to_db(new_event_dict):
    json_event = json.dumps(new_event_dict)
    event = Events(event=json_event, user_id=current_user.id)
    db.session.add(event)
    db.session.commit()


def create_wellness_event(submitted_log):
    return {
        'title': 'Wellness',
        'score': get_wellness_score(submitted_log),
        'date': str_fmt_date(submitted_log.date),
        'id': submitted_log.id
    }


def create_workout_event(submitted_log):
    return {
        'title': submitted_log.type,
        'score': submitted_log.grade,
        'date': str_fmt_date(submitted_log.date),
        'id': submitted_log.id
    }


def get_workout_week_num():
    last_workout = Weights.query.filter(
        Weights.user_id == current_user.id).order_by(
            Weights.id.desc()).first()
    template = Template.query.filter(
        Template.user_id == current_user.id).order_by(
            Template.id.desc()).first()

    if last_workout.workout_id == template.num_days:
        week = last_workout.workout_week + 1
    else:
        week = last_workout.workout_week
    return week


def get_workout_id():
    template = Template.query.filter(
        Template.user_id == current_user.id).order_by(
            Template.id.desc()).first()
    last_workout = Weights.query.filter(
        Weights.user_id == current_user.id).order_by(
            Weights.id.desc()).first()
    if last_workout.workout_id == template.num_days:
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
        existing_entry = Tag.query.filter(
            Tag.tag == str(entry), Tag.user_id == current_user.id).first()
        if existing_entry:
            tag_obj = existing_entry
        else:
            tag_obj = Tag(tag=str(entry), user_id=current_user.id)
        db_obj.tags.append(tag_obj)


# def create_id_dict():
#     all_days = [
#         date(2022, 1, 1) + timedelta(days=x)
#         for x in range((today - date(2022, 1, 1)).days + 5)
#     ]
#     for i, day in enumerate(all_days):
#         id_dict[day] = i
#         date_str_cal[str(day)] = id_dict[day]


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        name = registration_form.name.data
        username = registration_form.username.data
        hashed_password = generate_password_hash(
            registration_form.password1.data, "sha256")
        email = registration_form.email.data
        user_info = User(username=username,
                         name=name,
                         password_hash=hashed_password,
                         email=email,
                         user_id=current_user.id)
        db.session.add(user_info)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('registration.html', form=registration_form)


@app.route('/', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = User.query.filter_by(username=username).first()
        if user:
            passed = check_password_hash(user.password_hash, password)
            if passed:
                login_user(user)
                setup_oura_data()
                return redirect(url_for('log'))
            else:
                flash("Wrong password - try again.")
        else:
            flash("That user doesn't exist - try again...")
    return render_template('index.html', login_form=login_form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out.")
    return redirect(url_for('login'))


#TODO: figure out a better system for page_id
@app.route('/log',
           defaults={'page_id': get_page_id()},
           methods=['GET', 'POST'])
@app.route('/log/<int:page_id>', methods=['GET', 'POST'])
@login_required
def log(page_id):
    date = get_date(page_id)
    wellness_form = JournalForm()
    workout_form = WorkoutForm()
    sleep = Sleep.query.filter(Sleep.id == page_id,
                               Sleep.user_id == current_user.id).first()
    log = Log.query.filter(Log.id == page_id,
                           Log.user_id == current_user.id).first()
    readiness = Readiness.query.filter(
        Readiness.id == page_id, Readiness.user_id == current_user.id).first()
    workout = Workout.query.filter(Workout.id == page_id,
                                   Workout.user_id == current_user.id).first()
    new_template = Weights.query.filter(
        Weights.id == page_id, Weights.user_id == current_user.id).first()

    if wellness_form.validate_on_submit():
        user_id = current_user.id
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
                            stress=stress,
                            user_id=user_id)
        if selected_tags or added_tags:
            add_tags(added_tags, selected_tags, wellness_info)
        add_event_to_db(create_wellness_event(wellness_info))
        db.session.add(wellness_info)
        db.session.commit()
        if sleep:
            sleep.food_cutoff = wellness_form.food_cutoff.data
            db.session.add(sleep)
            db.session.commit()
        return redirect(url_for('log', page_id=page_id))

    if workout_form.validate_on_submit():
        file = request.files[str(workout_form.file.name)]
        type = workout_form.type.data
        if type == "Other":
            type = workout_form.specify_other.data
        soreness = workout_form.soreness.data
        grade = workout_form.grade.data
        workout_log = workout_form.workout_log.data
        workout_info = Workout(user_id=current_user.id,
                               data=file.read(),
                               date=date,
                               id=page_id,
                               filename=file.filename,
                               type=type,
                               soreness=soreness,
                               grade=grade,
                               workout_log=workout_log)
        if type == "Weights" and not new_template:
            current_template = get_current_template()
            get_weights_data(get_workout_id(), get_workout_week_num(), page_id,
                             current_template)
        add_event_to_db(create_workout_event(workout_info))
        db.session.add(workout_info)
        db.session.commit()
        return redirect(url_for('log', page_id=page_id))

    return render_template('log.html',
                           wellness_form=wellness_form,
                           workout_form=workout_form,
                           sleep=sleep,
                           log=log,
                           page_id=page_id,
                           date=format_date(date),
                           readiness=readiness,
                           workout=workout)


@app.route('/edit/<int:page_id>', methods=['GET', 'POST'])
@login_required
def edit_log(page_id):
    date = get_date(page_id)
    sleep = Sleep.query.filter(Sleep.user_id == current_user.id).get(page_id)
    readiness = Readiness.filter(
        Readiness.user_id == current_user.id).query.get(page_id)
    log = Log.query.filter(Log.user_id == current_user.id).get(page_id)
    workout = Workout.query.filter(
        Workout.user_id == current_user.id).get(page_id)
    if log:
        wellness_form = JournalForm(focus=log.focus,
                                    mood=log.mood,
                                    energy=log.energy,
                                    stress=log.stress,
                                    journal=log.journal,
                                    select_tags=log.tags,
                                    user_id=current_user.id)
    else:
        wellness_form = JournalForm()
    if workout:
        workout_form = WorkoutForm(soreness=workout.soreness,
                                   type=workout.type,
                                   specify_other=None,
                                   file=workout.data,
                                   grade=workout.grade,
                                   workout_log=workout.workout_log,
                                   user_id=current_user.id)
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
        add_event_to_db(create_workout_event(log))
        if sleep:
            sleep.food_cutoff = wellness_form.food_cutoff.data
            db.session.add(sleep)
            db.session.commit()
        return redirect(url_for('log', page_id=page_id))

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
        add_event_to_db(create_workout_event(workout))
        return redirect(url_for('log', page_id=page_id))
    return render_template('edit_post.html',
                           wellness_form=wellness_form,
                           workout_form=workout_form,
                           sleep=sleep,
                           page_id=page_id,
                           readiness=readiness,
                           date=date)


@app.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
    session['url'] = url_for('log', page_id=None)
    return render_template('calendar.html', events=get_db_events())


@app.route('/process', methods=['POST'])
@login_required
def process():
    ''' Used to process ajax call for calendar event clicks.
  Routes to the correct index page based on the page_id/dates.
  '''
    date_str = request.form.get('date_str')
    clicked_day_obj = Day.query.filter(Day.date_str == date_str).first()
    return redirect(url_for('log', page_id=clicked_day_obj.id))


@app.route('/download/<page_id>')
@login_required
def download(page_id):
    workout = Workout.query.filter_by(id=page_id,
                                      user_id=current_user.id).first()
    return send_file(BytesIO(workout.data),
                     attachment_filename=workout.filename,
                     as_attachment=True)


@app.route('/weights/<page_id>')
@login_required
def weights(page_id):
    this_week = Weights.query.filter_by(id=page_id,
                                        user_id=current_user.id).first()
    try:
        last_week = Weights.query.filter_by(
            workout_id=this_week.workout_id,
            template_id=this_week.template.id,
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
@login_required
def insights():
    filter_form = FilterForm()
    averages = get_overall_averages()
    total_days = len(
        Sleep.query.filter(Sleep.user_id == current_user.id).order_by(
            Sleep.id).all())
    filter_objs, filter_avgs, filtered_days = None, None, None
    if request.method == "POST":
        date_range = get_date_range(filter_form)
        filter_objs = get_filters(filter_form, date_range)
        filter_avgs = get_filtered_avgs(filter_objs)
        filtered_days = len(filter_objs)
    return render_template('insights.html',
                           averages=averages,
                           filter_form=filter_form,
                           filter_objs=filter_objs,
                           filter_avgs=filter_avgs,
                           filtered_days=filtered_days,
                           total_days=total_days)


@app.route('/template/<page_id>', methods=['GET', 'POST'])
@login_required
def template(page_id):
    template_form = TemplateForm()

    if request.method == "POST":
        rows = [
            template_form.day_one.data, template_form.day_two.data,
            template_form.day_three.data, template_form.day_four.data
        ]
        excs = [
            template_form.one_excs.data, template_form.two_excs.data,
            template_form.three_excs.data, template_form.four_excs.data
        ]
        template_data = Template(
            start_id=page_id,
            template_name=template_form.template_name.data,
            row_nums=rows,
            num_excs=excs,
            num_days=template_form.total_days.data,
            user_id=current_user.id)
        db.session.add(template_data)
        db.session.commit()
        current_template = get_current_template()
        get_weights_data(1, 1, page_id, current_template)
        return redirect(url_for('log', page_id=page_id))
    return render_template('update_template.html', template_form=template_form)
