import pytest
from ouraapp.insights.forms import FilterForm
from ouraapp.dashboard.models import Sleep
from ouraapp.insights.helpers import format_filters

FORM_DATA = {}


def test_format_filters(loaded_login):
    form = FilterForm()
    formatted_filter = format_filters(form=None)
    assert formatted_filter == Sleep.sleep_score > 70


#  filter_fields = {'sleep': ['']
#         'sleep': [
#             form.sleep_filter, form.sleep_operator, form.sleep_first,
#             form.sleep_second
#         ],
#         'readiness': [
#             form.readiness_filter, form.readiness_operator,
#             form.readiness_first, form.readiness_second
#         ],
#         'wellness': [
#             form.wellness_filter, form.wellness_operator, form.wellness_first,
#             form.wellness_second
#         ],
#         'workout': [
#             form.workout_filter, form.workout_operator, form.workout_first,
#             form.workout_second
#         ]
#     }
#  query_bases = {
#         'Sleep Score': 'sleep_score',
#         'Efficiency Score': 'efficiency_score',
#         'Readiness': 'readiness_score',
#         'Recovery Index': 'recover_index',
#         'Temperature Score': 'temperature_score',
#         'Focus': 'focus',
#         'Energy': 'energy',
#         'Mood': 'mood',
#         'Stress': 'stress',
#         'Grade': 'grade',
#         'Soreness': 'soreness'
