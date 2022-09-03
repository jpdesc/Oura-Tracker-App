import pytest
from ouraapp.weights_data import *
from ouraapp.routes import check_improvement
from ouraapp.database import Weights


def test_get_weights_data():
    output_data = get_weights_data(4, 1)
    assert 'Deadlift' == output_data[0][0]


def test_format_output():
    data = "['Calf Press']"
    assert format_output(data) == 'Calf Press'


def test_check_improvement():
    this_week = Weights.query.filter_by(id=116).first()
    last_week = Weights.query.filter_by(workout_id=this_week.workout_id,
                                        workout_week=this_week.workout_week -
                                        1).first()
    reps_improvement, weight_improvement = check_improvement(
        this_week, last_week)
    assert weight_improvement[0] == True
    assert weight_improvement[1] == False
    assert reps_improvement[2] == True
    assert reps_improvement[1] == False
