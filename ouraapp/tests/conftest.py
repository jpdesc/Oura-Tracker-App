from ouraapp import create_app
import pytest
import decorator
from flask.testing import FlaskClient


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    ctx = app.test_request_context()
    ctx.push()
    app.test_client_class = FlaskClient
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
