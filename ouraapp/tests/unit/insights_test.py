import pytest
from ouraapp.insights.forms import FilterForm
from ouraapp.dashboard.models import Sleep
from ouraapp.insights.helpers import format_filters
from flask import request
import json

# FORM_DATA = {{
#     'sleep_filter': 'Sleep Score',
#     'sleep_operator': '>',
#     'sleep_first': 70
# }}


def test_format_filters(loaded_login, loaded_db_client):
    data = {
        'sleep_filter': 'Sleep Score',
        'sleep_operator': '>',
        'sleep_first': 70
    }
    response = loaded_db_client.post('/insights', json=data)
    assert b"70" in response.data
