# import string
import os
# import re
# from google.oauth2 import service_account

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
    return BaseWorkout.query.filter_by(day_num=workout_id,
                                       template_id=template_id).first()

def get_weights_obj(page_id):
    weights = Weights.query.filter_by(user_id=current_user.id, day_id=page_id).first()
    return weights


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
    weights_obj = get_weights_obj(page_id)
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
    num_days = current_template.num_days
    if current_template.weights:
        weights = Weights.query.order_by(Weights.id).filter_by(user_id=current_user.id, template_id=current_template.id).all()
        idx = -1
        while not weights[idx].workout_id and len(weights) + idx > 0:
            db.session.delete(weights[idx])
            idx -= 1
        db.session.commit()

        last_workout = weights[idx]
        if last_workout.workout_id:
            if (int(last_workout.workout_id) + 1) <= num_days:
                return int(last_workout.workout_id) + 1
            else:
                logger.debug(f'id = 1')
                return 1
        return 1
    else:
        logger.debug('id=1')
        return 1


def get_workout_week_num():
    current_template = get_current_template()
    num_days = current_template.num_days
    if current_template.weights:
        weights = Weights.query.order_by(Weights.id).filter_by(user_id=current_user.id, template_id=current_template.id).all()
        idx = -1
        while not weights[idx].workout_week and len(weights) + idx > 0:
            db.session.delete(weights[idx])
            idx -= 1
        db.session.commit()

        last_workout = weights[idx]
        if last_workout.workout_id == num_days:
            week = last_workout.workout_week + 1
        else:
            week = last_workout.workout_week
    else:
        week = 1
    return week

def apply_toggle(weights, toggle):
    workout_num = weights.get_workout_num()
    total_days = weights.get_num_days()
    new_workout_num = workout_num + toggle
    next_week = total_days * weights.workout_week < new_workout_num
    prev_week = total_days * (weights.workout_week - 1) >= new_workout_num
    print(next_week)
    print(prev_week)
    if next_week:
        weights.workout_week = weights.workout_week + 1
        weights.workout_id = 1
    elif prev_week and weights.workout_week > 1:
        weights.workout_week = weights.workout_week - 1
        weights.workout_id = total_days
    else:
        if weights.workout_week > 1:
            weights.workout_id = weights.workout_id + toggle
    db.session.add(weights)
    db.session.commit()

def allow_toggle_check(weights):
    og_workout_num = weights.get_og_workout_num()
    workout_num = weights.get_workout_num()
    max_workout_num = weights.get_max_workout_num()

    left = True
    right = True

    if workout_num <= og_workout_num:
        left = False
    elif workout_num >= max_workout_num:
        right = False
    return left, right



def delete_exercises(weights_id):
    Exercise.query.filter_by(weights_id=weights_id).delete()
    db.session.commit()
# def load_template(weights):

    # weights.workout_id
    # print(new_workout_num)
    # print(new_workout_num // total_days)
    # print(new_workout_num % total_days)


def get_current_template():
    return Template.query.filter_by(user_id=current_user.id).order_by(
        Template.id.desc()).first()


def workout_data():
    weight_workouts = Weights.query.order_by(Weights.id).all()
    for workout in weight_workouts:
        matched = Workout.query.filter_by(day_id=workout.day_id, user_id=workout.user_id).first()
        if matched:
            matched.weights_data = True
            db.session.add(matched)
    db.session.commit()
