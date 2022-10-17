import json
import os
from datetime import date, timedelta, datetime
import time
from oura import OuraClient
from dotenv import load_dotenv
from flask_login import current_user
from ouraapp.models import Day
from .models import User
from ouraapp.dashboard.models import Sleep, Readiness
from ouraapp.calendar.models import Events
from ouraapp.extensions import db
import logging

logger = logging.getLogger("ouraapp")

#TODO: implement individual user


def pull_oura_data():
    ''' Pulls oura data from beginning of 2022 to today's date.'''
    load_dotenv()
    logger.debug(
        f'current_user.oura_access_token = {current_user.oura_access_token}')
    oura_token = current_user.oura_access_token
    # oura_token = os.getenv('OURA_PERSONAL_ACCESS_TOKEN')
    oura_client = OuraClient(personal_access_token=oura_token)
    start_date = date(2022, 1, 1)
    sleep_summary = oura_client.sleep_summary(start=str(start_date))
    readiness_summary = oura_client.readiness_summary(start=str(start_date))
    sleep_json = json.dumps(sleep_summary)
    readiness_json = json.dumps(readiness_summary)
    return [sleep_json, readiness_json]


def date_hook(json_dict):
    ''' Convert string object to datetime object within json dictionary using hook.

    This function will allow me to compare dates within broader calendar to sleep data
    in order to match up sleep data for a given date. If not a convertible string object,
    simply passes.
    '''
    key = 'summary_date'
    if key in json_dict:
        value = json_dict[key]
        json_dict[key] = datetime.strptime(value, '%Y-%m-%d')
    return json_dict


def format_date(date_obj):
    ''' Takes date string and converts to a date object, adding one
    day so that the sleep data from the previous night is aligned with
    current day.
    '''
    one_day_added = date_obj + timedelta(days=1)
    return one_day_added.date()


def convert_seconds(total_seconds):
    str_time = time.strftime("%H:%M",
                             time.gmtime(total_seconds))  # type: ignore
    return str_time


def add_event_to_db(new_event_dict):
    json_event = json.dumps(new_event_dict)
    event = Events(event=json_event, user_id=current_user.id)
    db.session.add(event)
    db.session.commit()


def add_sleep_to_db(json_dict):
    ''' Commit data to sleep database model.'''
    selected_data = json.loads(json_dict, object_hook=date_hook)
    logger.debug(
        f'User is authenticated: user obj = {User.query.filter_by(id=current_user.id).first()}'
    )
    for entry in (selected_data['sleep']):
        day = format_date(entry['summary_date'])
        db_day = Day.query.filter_by(date=day).first()
        logger.debug(
            f'{db_day.id}: - 1) Both user_id and sleep data are in database: {Sleep.query.filter_by(user_id = current_user.id, id=db_day.id).first()}'
        )
        logger.debug(
            f'{db_day.id}: - 2) user_id in database: {Sleep.query.filter_by(day_id=db_day.id).first()}'
        )
        if db.session.query(Sleep).filter_by(
                date=day, user_id=current_user.id).count() < 1:
            logger.debug(
                f'{db_day.id}: 3) Query says sleep obj should be added to db. {db_day.date}. Associated id: {db_day.id}.'
            )
            prev_night_data = Sleep(
                date=day,
                day_id=db_day.id,
                sleep_score=entry['score'],
                total_rem_sleep=convert_seconds(entry['rem']),
                total_deep_sleep=convert_seconds(entry['deep']),
                sleep_efficiency=entry['efficiency'],
                restlessness=entry['restless'],
                rem_score=entry['score_rem'],
                deep_score=entry['score_deep'],
                total_sleep=convert_seconds(entry['total']),
                seconds_sleep=entry['total'],
                user_id=current_user.id)
            # logger.debug(
            #     f'existing sleep obj in database: {database.Sleep.query.filter_by(id=id, user_id=current_user.id).first()}'
            # )
            add_event_to_db({
                'title': 'Sleep',
                'score': entry['score'],
                'date': day.strftime('%Y-%m-%d'),
                'id': db_day.id,
                'subclass': 'Oura'
            })
            db.session.add(prev_night_data)
    db.session.commit()


def add_readiness_to_db(json_dict):
    ''' Commit data to sleep database model.'''
    selected_data = json.loads(json_dict, object_hook=date_hook)
    for entry in (selected_data['readiness']):
        day = format_date(entry['summary_date'])
        db_day = Day.query.filter_by(date=day).first()
        if db.session.query(Readiness).filter_by(
                date=day, user_id=current_user.id).count() < 1:
            prev_night_data = Readiness(
                date=day,
                day_id=db_day.id,
                hrv_balance=entry['score_hrv_balance'],
                recovery_index=entry['score_recovery_index'],
                resting_hr=entry['score_resting_hr'],
                temperature=entry['score_temperature'],
                readiness_score=entry['score'],
                user_id=current_user.id)
            add_event_to_db({
                'title': 'Readiness',
                'score': entry['score'],
                'date': day.strftime('%Y-%m-%d'),
                'id': db_day.id,
                'subclass': 'Oura'
            })
            db.session.add(prev_night_data)
    db.session.commit()


def setup_oura_data():
    ''' Executes all functions relating to sleep data, adding data
    to databases.
    '''
    formatted_dicts = pull_oura_data()
    add_sleep_to_db(formatted_dicts[0])
    add_readiness_to_db(formatted_dicts[1])
