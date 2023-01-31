import re
from ouraapp.api import bp
from flask import request, abort, redirect, url_for
from ouraapp.dashboard.helpers import create_event
from ouraapp.weights.models import Weights, Exercise
from ouraapp.dashboard.models import Workout
from ouraapp.extensions import db
from flask_login import current_user
import logging

logger = logging.getLogger("ouraapp")


@bp.route('/api/data/<page_id>')
def data(page_id):

    query = Weights.query.filter_by(user_id=current_user.id,
                                    day_id=page_id).first()
    print([exercise.to_dict() for exercise in query.exercise_objs])
    return {
        'data': [exercise.to_dict() for exercise in query.exercise_objs],
    }


@bp.route('/api/data/<page_id>', methods=['POST'])
def update(page_id):
    data = request.get_json()
    if 'id' not in data:
        abort(400)
    exercise = Exercise.query.get(data['id'])
    for field in ['exercise_name', 'rep_range', 'sets', 'reps', 'weight']:
        if field in data:
            setattr(exercise, field, data[field])
            db.session.add(exercise)
            db.session.commit()

    return '', 204


@bp.route('/api/add_row/<page_id>')
def add_row(page_id):
    query = Weights.query.filter_by(day_id=page_id,
                                    user_id=current_user.id).first()
    blank_excs = Exercise(weights_id=query.id)
    db.session.add(blank_excs)
    db.session.commit()
    return '', 204


@bp.route('/api/remove_row/<page_id>')
def remove_row(page_id):
    query = Weights.query.filter_by(day_id=page_id,
                                    user_id=current_user.id).first()
    blanks = Exercise.query.filter_by(weights_id=query.id,
                                      exercise_name=None).all()
    if blanks:
        db.session.delete(blanks[-1])
        db.session.commit()

    return '', 204


#TODO: Move to weights module.
@bp.route('/api/process/<page_id>', methods=["POST"])
def process(page_id):
    workout = Workout.query.filter_by(day_id=page_id,
                                      user_id=current_user.id).first()
    if request.form:
        workout.soreness = request.form['soreness']
        workout.grade = request.form['grade']
    create_event(workout, 'Weights')
    db.session.add(workout)
    db.session.commit()
    return redirect(url_for('weights.weights', page_id=page_id))
