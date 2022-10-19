from ouraapp.calendar.models import Events
from ouraapp.models import Day
from ouraapp.dashboard.helpers import str_fmt_date
from flask_login import current_user


def event_exists(title, day_id):
    return Events.query.filter_by(day_id=day_id,
                                  title=title,
                                  user_id=current_user.id)


def create_weights_event(page_id):
    day = Day.query.filter_by(day_id=page_id)
    return {
        'title': 'Weights',
        'score': None,
        'date': str_fmt_date(day.date),
        'id': page_id
    }
