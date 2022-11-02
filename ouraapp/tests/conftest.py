import ouraapp
import run
import pytest
import decorator
from flask.testing import FlaskClient
from ouraapp.auth.models import User
from flask_login import login_user


@pytest.fixture()
def app():
    app = ouraapp.create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def app_ctx(app):
    with app.app_context():
        yield app


@pytest.fixture()
def client(app):
    ctx = app.test_request_context()
    ctx.push()
    app.test_client_class = FlaskClient
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def login(client):
    """Login helper function"""
    with client:
        user = User.query.filter_by(username='test').first()
        login_user(user)


# @pytest.fixture()
# def test_with_authenticated_user(app):
#     @login_manager.request_loader
#     def load_user_from_request(request):
#         return User.query.first()
