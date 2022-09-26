from flask_login import current_user
import json
from .models import Events


def get_db_events():
    '''Format events for use in the calendar.'''
    events = []
    events_objs = Events.query.filter(
        Events.user_id == current_user.id).order_by(Events.id).all()
    for event in events_objs:
        json_event = event.event
        event_dict = json.loads(json_event)
        events.append(event_dict)
    return events
