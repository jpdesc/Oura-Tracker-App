# import string
import os
# import re
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
from flask_login import current_user
from ouraapp.models import db
from .models import Weights, Template, BaseWorkout, Exercise
from ouraapp.dashboard.models import Workout
import logging

logger = logging.getLogger("ouraapp")
dir_path = os.path.dirname(os.path.realpath(__file__))


def get_next_base_workout(workout_id, template_id):
    # logger.debug(f'current_template.id = {get_current_template().id}')
    logger.debug(f'day_num = {get_workout_id()}')
    # logger.debug(
    #     f'type_current_template.id = {type(get_current_template().id)}')
    # logger.debug(f'type_current_template.id = {type(get_workout_id())}')
    # logger.debug(
    #     f'query result = {BaseWorkout.query.filter_by(day_num=get_workout_id(), template_id=get_current_template().id).first()}'
    # )
    return BaseWorkout.query.filter_by(day_num=workout_id,
                                       template_id=template_id).first()


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


def ensure_workout_log_exists(page_id):
    workout = Workout.query.filter_by(day_id=page_id,
                                      user_id=current_user.id).first()
    if not workout:
        new_workout = Workout(user_id=current_user.id,
                              day_id=page_id,
                              type="Weights")
        db.session.add(new_workout)
        db.session.commit()


def get_workout_id():
    current_template = get_current_template()
    print(f'current_template= {current_template}')
    num_days = current_template.num_days
    if current_template.weights:
        last_workout = Weights.query.filter_by(
            template_id=current_template.id).order_by(
                Weights.id.desc()).first()
        if last_workout.workout_id:
            if int(last_workout.workout_id) + 1 <= num_days:
                return int(last_workout.workout_id) + 1
        else:
            return 1
    else:
        return 1


def get_workout_week_num():
    current_template = get_current_template()
    num_days = current_template.num_days
    if current_template.weights:
        last_workout = Weights.query.filter_by(
            template_id=current_template.id).order_by(
                Weights.id.desc()).first()
        if last_workout.workout_id == num_days:
            week = last_workout.workout_week + 1
        else:
            week = last_workout.workout_week
    else:
        week = 1
    return week


def get_current_template():
    return Template.query.filter_by(user_id=current_user.id).order_by(
        Template.id.desc()).first()
