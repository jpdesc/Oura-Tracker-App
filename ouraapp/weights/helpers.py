# import string
import os
# import re
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
from flask_login import current_user
from ouraapp.models import db
from .models import Weights, Template, BaseWorkout, Exercise
from ouraapp.dashboard.models import Workout
from ouraapp.helpers import get_date
import logging

logger = logging.getLogger("ouraapp")
dir_path = os.path.dirname(os.path.realpath(__file__))


def get_next_base_workout(workout_id, template_id):
    # logger.debug(f'current_template.id = {get_current_template().id}')
    logger.debug(f'day_num = {workout_id}')
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
            try:
                exercise.weight_improve = int(exercise.weight) > int(
                    last_week_excs.weight)
            except ValueError:
                exercise.weight_improve = False
            try:
                exercise.reps_improve = int(exercise.weight) >= int(
                    last_week_excs.weight) and int(exercise.reps) > int(
                        last_week_excs.reps)
            except ValueError:
                exercise.reps_improve = False
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
    if workout:
        workout.weights_data = True
    else:
        workout = Workout(user_id=current_user.id,
                        weights_data=True,
                        day_id=page_id,
                        date=get_date(page_id),
                        type="Weights")
    db.session.add(workout)
    db.session.commit()
    return workout


def get_workout_id():
    current_template = get_current_template()
    logger.debug(f'current_template= {current_template}')
    num_days = current_template.num_days
    if current_template.weights:
        logger.debug(f'current_template.weights = True')
        last_workout = Weights.query.filter_by(
            template_id=current_template.id).order_by(
                Weights.id.desc()).first()
        logger.debug(f'last_workout = {last_workout}')
        if last_workout.workout_id:
            logger.debug(f'last_workout.workout_id exists')
            logger.debug(
                f'num_days = {num_days}, int(last_workout.workout_id) + 1 = {int(last_workout.workout_id) + 1}'
            )
            logger.debug(
                f'add new day execute = {(int(last_workout.workout_id) + 1) <= num_days}'
            )
            if (int(last_workout.workout_id) + 1) <= num_days:
                logger.debug(
                    f'last_workout_id + 1: {int(last_workout.workout_id) + 1}, add another day'
                )
                return int(last_workout.workout_id) + 1
            else:
                logger.debug(f'id = 1')
                return 1
    else:
        logger.debug('id=1')
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


def workout_data():
    weight_workouts = Weights.query.order_by(Weights.id).all()
    for workout in weight_workouts:
        matched = Workout.query.filter_by(day_id = workout.day_id, user_id=workout.user_id).all()
        matched.weights_data = True
        db.session.add(matched)
    db.session.commit()
