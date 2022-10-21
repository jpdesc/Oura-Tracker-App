import pytest
from ouraapp.dashboard.models import Readiness
from ouraapp.auth.helpers import setup_oura_data
# from run import app

#TODO: Mock testing.
setup_oura_data()


def test_readiness():
    readiness_db_class = Readiness.query.filter_by(id=100).first()
    for attr in readiness_db_class:
        assert attr != None
