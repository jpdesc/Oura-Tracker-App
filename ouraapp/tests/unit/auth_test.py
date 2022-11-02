import pytest
from ouraapp.dashboard.models import Readiness
from ouraapp.auth.helpers import pull_oura_data
from dotenv import load_dotenv
import os
from . import login_user, force_login
from flask_login import current_user
from ouraapp.extensions import db

# from run import app

#TODO: Mock testing.
# load_dotenv()

# def test_oura_api_call(mocker):
#     sleep_obj = open('sleep_data.txt', 'r')
#     sleep_data = sleep_obj.read()
#     sleep_obj.close()
#     readiness_obj = open('readiness_data.txt', 'r')
#     readiness_data = readiness_obj.read()
#     readiness_obj.close()
#     api_result = mocker.patch('setup_oura_data', [sleep_data, readiness_data])

# @force_login(cb=lambda s: login_user(s, 1))


# @force_login(cb=lambda s: login_user(s, 1))
def test_pull_oura_data(login):
    oura_data = pull_oura_data()
    assert oura_data
    assert oura_data[0][0][0]  #data in sleep category
    assert oura_data[1][0][0]  #data in readiness category

    # @force_login(cb=lambda s: login_user(s, 1))
    # def test_login(client, login):

    #     assert current_user.id == 1

    # def test_readiness(mocker):
    # readiness_db_class = Readiness.query.filter_by(id=100).first()
    # for attr in readiness_db_class:
    #     assert attr != None
