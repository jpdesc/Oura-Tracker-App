import pytest
from ouraapp.database import Readiness
from ouraapp.fetch_oura_data import setup_oura_data

setup_oura_data()


def test_readiness():
    readiness_db_class = Readiness.query.filter_by(id=100).first()
    for attr in readiness_db_class:
        assert attr != None
