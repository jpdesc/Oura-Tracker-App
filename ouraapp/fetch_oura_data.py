import json
import os
from datetime import date, timedelta, datetime
import time
from oura import OuraClient
from dotenv import load_dotenv
from ouraapp import database
from ouraapp import db

today = date.today()
date_str_cal = {}


def pull_oura_data():
    ''' Pulls oura data from beginning of 2022 to today's date.'''
    load_dotenv()
    oura_token = os.getenv('OURA_PERSONAL_ACCESS_TOKEN')
    oura_client = OuraClient(personal_access_token=oura_token)
    start_date = date(2022, 1, 1)
    end_date = date.today()
    sleep_summary = oura_client.sleep_summary(start=str(start_date))
    readiness_summary = oura_client.readiness_summary(start=str(start_date))
    all_days = [
        start_date + timedelta(days=x)
        for x in range((end_date - start_date).days + 500)
    ]
    for i, day in enumerate(all_days):
        id_dict[day] = i
    sleep_json = json.dumps(sleep_summary)
    readiness_json = json.dumps(readiness_summary)
    return [sleep_json, readiness_json]


def create_id_dict():
    id_dict = {}
    all_days = [
        date(2022, 1, 1) + timedelta(days=x)
        for x in range((today - date(2022, 1, 1)).days + 5)
    ]
    for i, day in enumerate(all_days):
        id_dict[day] = i
        date_str_cal[str(day)] = id_dict[day]
    return id_dict


id_dict = create_id_dict()


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
    # print(total_seconds)
    str_time = time.strftime("%H:%M",
                             time.gmtime(total_seconds))  # type: ignore
    return str_time


def add_sleep_to_db(json_dict):
    ''' Commit data to sleep database model.'''
    selected_data = json.loads(json_dict, object_hook=date_hook)
    for entry in (selected_data['sleep']):
        day = format_date(entry['summary_date'])
        # print(selected_data)
        if db.session.query(database.Sleep).filter_by(date=day).count() < 1:
            # obj = Sleep.query.filter_by(date=day).first()
            # if obj:
            #     obj.seconds_sleep = entry['total']
            #     obj.sleep_score = entry['score']
            prev_night_data = database.Sleep(
                date=day,
                id=id_dict[day],
                sleep_score=entry['score'],
                total_rem_sleep=convert_seconds(entry['rem']),
                total_deep_sleep=convert_seconds(entry['deep']),
                sleep_efficiency=entry['efficiency'],
                restlessness=entry['restless'],
                rem_score=entry['score_rem'],
                deep_score=entry['score_deep'],
                total_sleep=convert_seconds(entry['total']),
                seconds_sleep=entry['total'])
            db.session.add(prev_night_data)
    db.session.commit()


def add_readiness_to_db(json_dict):
    ''' Commit data to sleep database model.'''
    selected_data = json.loads(json_dict, object_hook=date_hook)
    for entry in (selected_data['readiness']):
        day = format_date(entry['summary_date'])
        if db.session.query(
                database.Readiness).filter_by(date=day).count() < 1:
            try:
                resting_hr_score = entry['score_resting_hr']
            except KeyError:
                resting_hr_score = 75
            prev_night_data = database.Readiness(
                date=day,
                id=id_dict[day],
                hrv_balance=entry['score_hrv_balance'],
                recovery_index=entry['score_recovery_index'],
                resting_hr=resting_hr_score,
                temperature=entry['score_temperature'],
                readiness_score=entry['score'])
            db.session.add(prev_night_data)
    db.session.commit()


def setup_oura_data():
    ''' Executes all functions relating to sleep data, adding data
    to databases.
    '''
    formatted_dicts = pull_oura_data()
    add_sleep_to_db(formatted_dicts[0])
    add_readiness_to_db(formatted_dicts[1])
