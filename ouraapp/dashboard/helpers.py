import json
from datetime import date
from flask_login import current_user
from ouraapp.format import str_fmt_date
from ouraapp.models import Day
from ouraapp.helpers import get_date
from .models import Tag
from ouraapp.calendar.models import Events
from ouraapp.weights.models import Weights, Exercise
from ouraapp.dashboard.models import Workout
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


# def event_exists(title, day_id):
#     return Events.query.filter_by(day_id=day_id,
#                                   title=title,
#                                   user_id=current_user.id).first()


def create_event(submitted_log, title):
    event = Events.query.filter_by(user_id=current_user.id,
                                   day_id=submitted_log.id,
                                   title=title).first()
    if not event:
        event = Events()
    event.title = title
    if title == 'Wellness':
        event.score = get_wellness_score(submitted_log)
    elif title == 'Sleep':
        event.score = submitted_log.sleep_score
        event.subclass = 'Oura'
    elif title == 'Readiness':
        event.score = submitted_log.readiness_score
        event.subclass = 'Oura'
    else:
        event.score = submitted_log.grade
    event.day_id = submitted_log.day_id
    event.date = get_date(submitted_log.day_id)
    event.user_id = current_user.id
    db.session.add(event)
    db.session.commit()


def get_rid_of_bonus_events():
    all_days = Day.query.order_by(id).all()
    for day in all_days:
        titles = {}
        events = Events.query.filter_by(user_id=1, day_id=day.id).all()
        for event in events:
            if event.title not in titles:
                titles[event.title] = 1
            else:
                db.session.delete(event)
    db.session.commit()


# def create_workout_event(submitted_log):
#     return {
#         'title': submitted_log.type,
#         'score': submitted_log.grade,
#         'date': str_fmt_date(submitted_log.date),
#         'id': submitted_log.id
#     }

# def create_weights_event(page_id, score):
#     day = Day.query.filter_by(id=page_id).first()
#     return {
#         'title': 'Weights',
#         'score': score,
#         'date': str_fmt_date(day.date),
#         'id': page_id
#     }

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

# def add_event_to_db(title, page_id, existing_event):
#     if existing_event:
#         existing_event.event = json_event
#         db.session.add(existing_event)
#         logger.debug('editing existing event.')
#     else:
#         logger.debug('creating new event.')
#         event = Events(event=json_event,
#                        day_id=page_id,
#                        title=title,
#                        user_id=current_user.id)
#         db.session.add(event)
#     db.session.commit()

# def add_title_and_day():
#     all_events = Events.query.order_by(Events.id).all()
#     for event in all_events:
#         if event.event:
#             dict = json.loads(event.event)
#             event.title = dict['title']
#             event.day_id = int(dict['id'])
#             db.session.add(event)
#             db.session.commit()

# def remove_extra_events():
#     all_events = Events.query.order_by(Events.day_id).all()
#     for event in all_events:
#         if event.event:
#             dict = json.loads(event.event)
#             event.title = dict['title']
#             event.day_id = int(dict['id'])
#             db.session.add(event)
#             db.session.commit()


def clear_workout(page_id):
    weights = Weights.query.filter_by(day_id=page_id,
                                      user_id=current_user.id).first()
    exercise = Exercise.query.filter_by(weights_id=weights.id).delete()
    workout = Workout.query.filter_by(day_id=page_id,
                                      user_id=current_user.id).delete()
    event = Events.query.filter_by(day_id=page_id,
                                   user_id=current_user.id).delete()
    db.session.delete(weights)
    db.session.commit()
