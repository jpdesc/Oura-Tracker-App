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


def test_insights_post_response__logged_in(loaded_db_client, loaded_login):
    data = {
        'sleep_filter': 'Sleep Score',
        'sleep_operator': '>',
        'sleep_first': 70
    }
    response = loaded_db_client.post('/insights', json=data)
    assert response.status_code == 200


# sleep_filter = SelectField('Sleep ',
#                                choices=[
#                                    '', 'Sleep Score', 'Efficiency Score',
#                                    'Food Timing 0-1.5', 'Food Timing 1.5-3',
#                                    'Food Timing 3-4.5', 'Food Timing 4.5+'
#                                ])
#     sleep_operator = SelectField(
#         choices=['', '>', '<', 'between'],
#         render_kw={'onchange': "secondField('sleep_second')"})
#     sleep_first = IntegerField()
