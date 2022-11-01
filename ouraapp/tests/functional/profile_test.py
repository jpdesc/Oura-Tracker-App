from . import force_login, login_user


@force_login(cb=lambda s: login_user(s, 1))
def test_edit_profile_response(client):
    response = client.get('/profile/1')
    assert response.status_code == 200
    # assert b"Workout" in response.data


@force_login(cb=lambda s: login_user(s, 1))
def test_show_profile_response__logged_in(client):
    response = client.get('/profile/0')
    assert response.status_code == 200


def test_show_profile_response__logged_out(client):
    response = client.get('/profile/0')
    assert response.status_code == 302
    assert b"Redirecting..." in response.data
