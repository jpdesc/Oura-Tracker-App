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
    events = Events.query.filter_by(user_id=current_user.id,
                                   day_id=submitted_log.day_id,
                                   title=title).all()
    for event in events:
        db.session.delete(event)
        db.session.commit()

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
    all_days = Day.query.order_by(Day.id).all()
    for day in all_days:
        titles = {}
        events = Events.query.filter_by(user_id=1, day_id=day.id).all()
        for event in events:
            if event.title not in titles:
                titles[event.title] = 1
            else:
                db.session.delete(event)
    db.session.commit()


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
