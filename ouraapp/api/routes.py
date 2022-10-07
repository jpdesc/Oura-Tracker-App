from ouraapp.api import bp
from flask import request, abort, redirect, url_for, render_template, flash
from ouraapp.weights.models import Weights, Exercise
from ouraapp.extensions import db
from flask_login import current_user


@bp.route('/api/data/<page_id>')
def data(page_id):
    query = Weights.query.filter_by(user_id=current_user.id,
                                    day_id=page_id).first()
    print('data')
    return {
        'data': [exercise.to_dict() for exercise in query.exercises],
    }


@bp.route('/api/data/<page_id>', methods=['POST'])
def update(page_id):
    print('update')
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
    print('add_row')
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
    else:
        flash('No more blank rows to delete.')
    print('remove_row')
    return '', 204
