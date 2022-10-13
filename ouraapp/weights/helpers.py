# import string
import os
# import re
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
from flask_login import current_user
from ouraapp.models import db
from ouraapp.dashboard.helpers import get_workout_id, get_current_template
from .models import Weights, Template, BaseWorkout, Exercise
import logging

logger = logging.getLogger("ouraapp")
dir_path = os.path.dirname(os.path.realpath(__file__))


def get_next_base_workout():
    # logger.debug(f'current_template.id = {get_current_template().id}')
    # logger.debug(f'day_num = {get_workout_id()}')
    # logger.debug(
    #     f'type_current_template.id = {type(get_current_template().id)}')
    # logger.debug(f'type_current_template.id = {type(get_workout_id())}')
    # logger.debug(
    #     f'query result = {BaseWorkout.query.filter_by(day_num=get_workout_id(), template_id=get_current_template().id).first()}'
    # )
    return BaseWorkout.query.filter_by(
        day_num=get_workout_id(),
        template_id=get_current_template().id).first()


def check_improvement(this_week, last_week_id):
    exercise_list = []
    for exercise in this_week:
        last_week_excs = Exercise.query.filter_by(
            weights_id=last_week_id,
            exercise_name=exercise.exercise_name).first()
        if last_week_excs:
            exercise.weight_improve = int(exercise.weight) > int(
                last_week_excs.weight)
            exercise.reps_improve = int(exercise.weight) >= int(
                last_week_excs.weight) and int(exercise.reps) > int(
                    last_week_excs.reps)
        db.session.add(exercise)
        exercise_list.append(exercise)
    db.session.commit()
    return exercise_list


def clear_exercises(page_id):
    weights_obj = Weights.query.filter_by(day_id=page_id,
                                          user_id=current_user.id).first()
    if weights_obj.exercises:
        for exercise in weights_obj.exercises:
            db.session.delete(exercise)
        db.session.commit()


def convert_older_weights():
    all_weights = Weights.query.order_by(id).all()
    for weight in all_weights:
        for i, exercise in enumerate(weight.exercises):
            add_exercise = Exercise(
                day_id=weight.day_id,
                weights_id=weight.id,
            )


#             class Weights(db.Model):
#     __tablename__ = 'weights'
#     id = db.Column(db.Integer, primary_key=True)
#     day_id = db.Column(db.Integer)
#     exercises = db.Column(db.ARRAY(db.String))
#     exercises_old = db.Column(db.ARRAY(db.String))
#     set_ranges = db.Column(db.ARRAY(db.String))
#     reps = db.Column(db.ARRAY(db.String))
#     weight = db.Column(db.ARRAY(db.String))
#     subbed = db.Column(db.String)
#     workout_id = db.Column(db.Integer)
#     workout_week = db.Column(db.Integer)
#     template_id = db.Column(db.Integer, db.ForeignKey('template.id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     base_id = db.Column(db.Integer, db.ForeignKey('base_workout.id'))
#     exercises = db.relationship('Exercise', backref='weights')

# class Exercise(db.Model):
#     __tablename__ = 'exercise'
#     id = db.Column(db.Integer, primary_key=True)
#     day_id = db.Column(db.Integer)
#     exercise_name = db.Column(db.String)
#     sets = db.Column(db.String)
#     rep_range = db.Column(db.String)
#     reps = db.Column(db.String)
#     reps_improve = db.Column(db.Boolean)
#     weight = db.Column(db.String)
#     weight_improve = db.Column(db.Boolean)
#     weights_id = db.Column(db.Integer, db.ForeignKey('weights.id'))
