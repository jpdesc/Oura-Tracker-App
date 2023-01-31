from . import force_login, login_user
from ouraapp.auth.helpers import setup_oura_data


@force_login(cb=lambda s: login_user(s, 1))
def test_weights__logged_in(loaded_db_client):
    response = loaded_db_client.get('/workout/weights/306')
    assert response.status_code == 200


def test_weights__logged_out(loaded_db_client):
    response = loaded_db_client.get('/workout/weights/306')
    assert response.status_code == 302


@force_login(cb=lambda s: login_user(s, 1))
def test_edit_weights__logged_in(loaded_db_client):
    response = loaded_db_client.get('/workout/edit_weights/from_base:True/306')
    assert response.status_code == 200
    response = loaded_db_client.get('/workout/edit_weights/from_base:False/306')
    assert response.status_code == 200


def test_edit_weights__logged_out(loaded_db_client):
    response = loaded_db_client.get('/workout/edit_weights/from_base:True/306')
    assert response.status_code == 302
    response = loaded_db_client.get('/workout/edit_weights/from_base:False/306')
    assert response.status_code == 302


@force_login(cb=lambda s: login_user(s, 1))
def test_create_template__logged_in(loaded_db_client):
    response = loaded_db_client.get('/workout/create_template/test/1/306')
    assert response.status_code == 200


def test_create_template__logged_out(loaded_db_client):
    response = loaded_db_client.get('/workout/create_template/test/1/306')
    assert response.status_code == 302


@force_login(cb=lambda s: login_user(s, 1))
def test_init_template__logged_in(loaded_db_client):
    response = loaded_db_client.get('/workout/create_template/test/1/306')
    assert response.status_code == 200


def test_init_template__logged_out(loaded_db_client):
    response = loaded_db_client.get('/workout/create_template/test/1/306')
    assert response.status_code == 302
