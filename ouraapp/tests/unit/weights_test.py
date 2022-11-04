import pytest
from ouraapp.weights.helpers import check_improvement
from ouraapp.weights.models import Weights, Exercise
from flask_login import current_user


def test_check_improvement(loaded_login):
    this_week = Weights.query.filter_by(day_id=306, user_id=1).first()
    this_week_excs = Exercise.query.filter(
        Exercise.weights_id == this_week.id,
        Exercise.exercise_name != None).all()
    last_week = Weights.query.filter_by(
        workout_id=this_week.workout_id,
        template_id=this_week.template.id,
        workout_week=(int(this_week.workout_week) - 1)).first()
    exercise_list = check_improvement(this_week_excs, last_week.id)
    weight_improve_count = 0
    reps_improve_count = 0
    for excs in exercise_list:
        if excs.weight_improve == True:
            weight_improve_count += 1
        elif excs.reps_improve == True:
            reps_improve_count += 1
    assert weight_improve_count == 4
    assert reps_improve_count == 0

    # assert weight_improvement[0] == True
    # assert weight_improvement[1] == False
    # assert reps_improvement[2] == True
    # assert reps_improvement[1] == False
