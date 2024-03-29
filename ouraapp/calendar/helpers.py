from flask_login import current_user
import json
from ouraapp.format import date_fmt_str
from ouraapp.extensions import db
from .models import Events


def get_db_events():
    '''Format events for use in the calendar.'''
    events = Events.query.filter_by(user_id=current_user.id).all()
    return events


def db_event_fix():
    events = Events.query.filter_by(user_id=1).all()
    for event in events:
        if event.event:
            event_dict = json.loads(event.event)
            event.score = event_dict['score']
            event.date = date_fmt_str(event_dict['date'])
            event.title = event_dict['title']
        if event.title == 'Readiness' or event.title == 'Sleep':
            event.subclass = 'Oura'
        db.session.add(event)
    db.session.commit()
