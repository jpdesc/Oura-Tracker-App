import json
from datetime import date
from flask_login import current_user
from ouraapp.format import str_fmt_date
from ouraapp.models import Day
from .models import Tag
from ouraapp.calendar.models import Events
from ouraapp.weights.models import Weights, Template
from ouraapp import db
import logging

logger = logging.getLogger("ouraapp")


def get_date(page_id):
    db_obj = Day.query.filter_by(id=page_id).first()
    return db_obj.date


def get_wellness_score(log):
    if log.stress:
        return (int(log.focus) + int(log.mood) + int(log.energy) +
                (6 - int(log.stress))) / 4
    else:
        return None


def get_tags(added_tags, selected_tags):
    tags = []
    if added_tags:
        for word in added_tags.split(','):
            stripped = word.strip(', ').lower()
            tags.append(stripped)
    if selected_tags:
        for tag in selected_tags:
            if tag not in tags:
                tags.append(tag)
    return tags


def add_tags(added_tags, selected_tags, db_obj):
    for entry in get_tags(added_tags, selected_tags):
        existing_entry = Tag.query.filter(
            Tag.tag == str(entry), Tag.user_id == current_user.id).first()
        if existing_entry:
            tag_obj = existing_entry
        else:
            tag_obj = Tag(tag=str(entry), user_id=current_user.id)
        db_obj.tags.append(tag_obj)


def event_exists(title, day_id):
    return Events.query.filter_by(day_id=day_id,
                                  title=title,
                                  user_id=current_user.id)


def create_wellness_event(submitted_log):
    return {
        'title': 'Wellness',
        'score': get_wellness_score(submitted_log),
        'date': str_fmt_date(submitted_log.date),
        'id': submitted_log.id
    }


def create_workout_event(submitted_log):
    return {
        'title': submitted_log.type,
        'score': submitted_log.grade,
        'date': str_fmt_date(submitted_log.date),
        'id': submitted_log.id
    }


def create_weights_event(page_id):
    day = Day.query.filter_by(day_id=page_id)
    return {
        'title': 'Weights',
        'score': None,
        'date': str_fmt_date(day.date),
        'id': page_id
    }


# def create_all_cal_events():
#     wellness = Log.query.order_by(Log.id).all()
#     for a in wellness:
#         add_event_to_db(create_wellness_event(a))

#     workout = Workout.query.order_by(Workout.id).all()
#     for b in workout:
#         add_event_to_db(create_workout_event(b))

#     sleep = Sleep.query.order_by(Sleep.id).all()
#     for c in sleep:
#         add_event_to_db({
#             'title': 'Sleep',
#             'score': c.sleep_score,
#             'date': c.date.strftime('%Y-%m-%d'),
#             'id': c.id,
#             'subclass': 'Oura'
#         })
#     readiness = Readiness.query.order_by(Readiness.id).all()
#     for d in readiness:
#         add_event_to_db({
#             'title': 'Readiness',
#             'score': d.readiness_score,
#             'date': d.date.strftime('%Y-%m-%d'),
#             'id': d.id,
#             'subclass': 'Oura'
#         })








def add_event_to_db(new_event_dict, page_id, existing_event):
    title = new_event_dict['title']
    json_event = json.dumps(new_event_dict)
    if existing_event:
        existing_event.event = json_event
        db.session.add(existing_event)
    else:
        event = Events(event=json_event,
                       day_id=page_id,
                       title=title,
                       user_id=current_user.id)
        db.session.add(event)
    db.session.commit()


def add_title_and_day():
    all_events = Events.query.order_by(Events.id).all()
    for event in all_events:
        if event.event:
            dict = json.loads(event.event)
            event.title = dict['title']
            event.day_id = int(dict['id'])
            db.session.add(event)
            db.session.commit()


# def remove_extra_events():
#     all_events = Events.query.order_by(Events.day_id).all()
#     for event in all_events:
#         if event.event:
#             dict = json.loads(event.event)
#             event.title = dict['title']
#             event.day_id = int(dict['id'])
#             db.session.add(event)
#             db.session.commit()
