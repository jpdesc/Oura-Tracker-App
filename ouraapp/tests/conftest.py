from ouraapp.extensions import db
import run
import ouraapp
import pytest
import decorator
from flask.testing import FlaskClient
from ouraapp.auth.models import User
from flask_login import login_user
import os
from ouraapp.extensions import db
from datetime import date
from ouraapp.helpers import update_days_db
from ouraapp.auth.routes import setup_oura_data


@pytest.fixture()
def app():
    app = ouraapp.create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.getenv('TEST_DATABASE_URL')
    })
    with app.app_context():
        db.create_all()
        create_user()
        update_days_db()
        # print(User.query.all())
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def loaded_db_app():
    full_app = ouraapp.create_app()
    full_app.config.update({"TESTING": True})
    with full_app.app_context():
        yield full_app


def create_user(access_token=True):
    user = User(email='server.jpdesc@gmail.com',
                username='test',
                password='test',
                name='test',
                oura_access_token=os.getenv("OURA_PERSONAL_ACCESS_TOKEN"),
                join_date=date.today())
    if access_token is False:
        user.oura_access_token = None
    db.session.add(user)
    db.session.commit()


@pytest.fixture()
def client(app):
    ctx = app.test_request_context()
    ctx.push()
    app.test_client_class = FlaskClient
    # print(User.query.all())
    return app.test_client()


@pytest.fixture()
def loaded_db_client(loaded_db_app):
    # setup_oura_data()
    ctx = loaded_db_app.test_request_context()
    ctx.push()
    loaded_db_app.test_client_class = FlaskClient
    # print(User.query.all())
    return loaded_db_app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def login(client):
    """Login helper function"""
    user = User.query.filter_by(username='test').first()
    login_user(user)
    # print(user)


@pytest.fixture()
def loaded_login(loaded_db_client):
    user = User.query.filter_by(username='test').first()
    login_user(user)


# @pytest.fixture()
# def data_loaded_login(data_loaded_client):
#     """Login helper function"""
#     user = User.query.filter_by(username='test').first()
#     login_user(user)

# @pytest.fixture()
# def test_with_authenticated_user(app):
#     @login_manager.request_loader
#     def load_user_from_request(request):
#         return User.query.first()
