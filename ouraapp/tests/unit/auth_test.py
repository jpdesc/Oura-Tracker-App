import pytest
from ouraapp.dashboard.models import Readiness
from ouraapp.auth.helpers import setup_oura_data
from dotenv import load_dotenv
import os

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


# def test_readiness(mocker):
#     mocker.patch.object(ouraapp.auth.helpers, 'oura_token',
#                         os.getenv('OURA_PERSONAL_ACCESS_TOKEN'))
#     readiness_db_class = Readiness.query.filter_by(id=100).first()
#     for attr in readiness_db_class:
#         assert attr != None
