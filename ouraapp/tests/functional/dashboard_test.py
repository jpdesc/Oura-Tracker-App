from decorator import decorator
from flask.testing import FlaskClient
from . import force_login, login_user
import requests
import json


@force_login(cb=lambda s: login_user(s, 1))
def test_dashboard_response(client):
    response = client.get('/dashboard/log/280')
    assert response.status_code == 200
    assert b"Workout" in response.data


@force_login(cb=lambda s: login_user(s, 1))
def test_edit_response(client):
    response = client.get('/dashboard/edit/280')
    assert response.status_code == 200


def test_not_logged_in_dashboard_response(client):
    response = client.get('/dashboard/log')
    assert response.status_code == 302


def test_not_logged_in_edit_response(client):
    response = client.get('/dashboard/edit/280')
    assert response.status_code == 302
