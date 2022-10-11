# import string
import os
# import re
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
from flask_login import current_user
from ouraapp.models import db
from ouraapp.dashboard.helpers import get_workout_id
from .models import Weights, Template, BaseWorkout, Exercise

dir_path = os.path.dirname(os.path.realpath(__file__))


def get_next_base_workout():
    return BaseWorkout.query.filter_by(day_num=get_workout_id()).first()


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
