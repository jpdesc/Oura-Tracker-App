import pytest
from ouraapp.dashboard.models import Readiness, Sleep
from ouraapp.auth.helpers import pull_oura_data, setup_oura_data
from dotenv import load_dotenv
import os
from . import login_user, force_login
from flask_login import current_user
from ouraapp.extensions import db


def test_pull_oura_data(login):
    oura_data = pull_oura_data()
    setup_oura_data()
    readiness = Readiness.query.all()
    sleep = Sleep.query.all()
    assert oura_data
    assert oura_data[0][0][0]  #data in sleep category
    assert oura_data[1][0][0]  #data in readiness category
    assert len(readiness) > 0
    assert len(sleep) > 0
    assert readiness[0].date
    assert sleep[0].sleep_score
