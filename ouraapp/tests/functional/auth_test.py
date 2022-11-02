from flask import request, url_for
from . import force_login, login_user


def test_registration_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the registration page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get('/auth/register')
    assert response.status_code == 200


def test_login_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get('/auth/login')
    assert response.status_code == 200


def test_logout_redirect(client):
    response = client.get('/auth/logout')
    assert response.status_code == 302


@force_login(cb=lambda s: login_user(s, 1))
def test_index_page__logged_in(client):
    '''
    Test redirect if user is logged in.
    '''
    response = client.get('/')
    assert response.status_code == 302


@force_login(cb=lambda s: login_user(s, None))
def test_index_page__logged_out(client):
    '''
    Test no redirect if user is not logged in.
    '''
    response = client.get('/')
    assert response.status_code == 200
    assert b"password" in response.data
