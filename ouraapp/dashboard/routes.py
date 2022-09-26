from io import BytesIO
from flask import render_template, redirect, url_for, request, send_file, Blueprint
from ouraapp.weights.helpers import get_weights_data, get_current_template
from ouraapp.weights.models import Weights
from .models import Sleep, Log, Readiness, Workout
from .helpers import add_event_to_db, get_date, add_tags, create_wellness_event, create_workout_event, get_workout_id, get_workout_week_num
from ouraapp.helpers import get_page_id
from ouraapp.format import format_date
from flask_login import login_required, current_user
from .forms import JournalForm, WorkoutForm
from ouraapp.extensions import db
from ouraapp.dashboard import bp
import logging

logger = logging.getLogger("ouraapp")


@bp.route('/log', defaults={'page_id': get_page_id()}, methods=['GET', 'POST'])
@bp.route('/log/<int:page_id>', methods=['GET', 'POST'])
@login_required
def log(page_id):
    # logger.debug(
    #     f'User is authenticated: user id = {User.query.filter_by(id=current_user.id)}'
    # )

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
        # if sleep:
        #     sleep.food_cutoff = wellness_form.food_cutoff.data
        #     db.session.add(sleep)
        #     db.session.commit()
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


@bp.route('/edit/<int:page_id>', methods=['GET', 'POST'])
@login_required
def edit_log(page_id):
    date = get_date(page_id)
    sleep = Sleep.query.filter(Sleep.user_id == current_user.id,
                               Sleep.id == page_id).first()
    readiness = Readiness.query.filter(Readiness.user_id == current_user.id,
                                       Readiness.id == page_id).first()
    log = Log.query.filter(Log.user_id == current_user.id,
                           Log.id == page_id).first()
    workout = Workout.query.filter(Workout.user_id == current_user.id,
                                   Workout.id == page_id).first()
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
        add_event_to_db(create_workout_event(log))
        # if sleep:
        #     sleep.food_cutoff = wellness_form.food_cutoff.data
        #     db.session.add(sleep)
        #     db.session.commit()
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
    return render_template('dashboard/edit_post.html',
                           wellness_form=wellness_form,
                           workout_form=workout_form,
                           sleep=sleep,
                           page_id=page_id,
                           readiness=readiness,
                           date=date)


@bp.route('/download/<page_id>')
@login_required
def download(page_id):
    workout = Workout.query.filter_by(id=page_id,
                                      user_id=current_user.id).first()
    return send_file(BytesIO(workout.data),
                     attachment_filename=workout.filename,
                     as_attachment=True)
