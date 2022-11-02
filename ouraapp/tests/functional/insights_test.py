from . import force_login, login_user
from ouraapp.auth.helpers import setup_oura_data


@force_login(cb=lambda s: login_user(s, 1))
def test_insights_response__logged_in(client, login):
    with client:
        setup_oura_data()
    response = client.get('/insights')
    assert response.status_code == 200


def test_insights_response__logged_out(client):
    response = client.get('/insights')
    assert response.status_code == 302
