import json
from json import JSONEncoder
import os
from datetime import date, timedelta, datetime, time
import time
from oura import OuraClient
from dotenv import load_dotenv
from app import Sleep, db

    
# Keys which have categories that I will not use in my app. 
delete_keys = ["period_id", "is_longest", "timezone", "bedtime_end", "bedtime_start", \
            "breath_average", "duration", "awake", "light", "midpoint_time", \
            "onset_latency", "hr_5min", "hr_average", "hr_lowest", "hypnogram_5min", "rmssd", \
            "rmssd_5min", "score", "score_alignment", "score_disturbances", \
            "score_efficiency", "score_latency", "temperature_deviation", \
            "temperature_trend_deviation", "bedtime_start_delta", "bedtime_end_delta", \
            "midpoint_at_delta", "temperature_delta"]

id_dict = {}

def pull_oura_data():
    '''pulls oura data from beginning of 2022 to today's date.'''
    load_dotenv()
    oura_token = os.getenv('OURA_PERSONAL_ACCESS_TOKEN')
    oura_client = OuraClient(personal_access_token=oura_token)
    start_date = date(2022, 1, 1)
    end_date = date.today()
    data_period = str(end_date - start_date) # define period from which to pull data. 
    sleep_summary = oura_client.sleep_summary(start=data_period)
    all_days = [start_date + timedelta(days=x) for x in range((end_date-start_date).days + 500)]
    for i, day in enumerate(all_days):
        id_dict[day] = i


    #FIXME: no need to write to file here. 
    with open('result.json', 'w') as file:
        data = json.dump(sleep_summary, file)
    with open('result.json', 'r') as file:
        data = json.loads(file.read())
    for day in data['sleep']:
        for key in delete_keys:
            if key in day:
                del day[key]
    with open('new_result.json', 'w') as file:
        json.dump(data, file, indent=2)

def date_hook(json_dict):
    """ Convert string object to datetime object within json dictionary using hook. 

    This function will allow me to compare dates within broader calendar to sleep data
    in order to match up sleep data for a given date. If not a convertible string object,
    simply passes.
    """
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = date.strptime(value, '%Y-%m-%d')
        except:
            pass
    return json_dict

def convert_json_data():
    ''' Convert API data to properly formatted json data. 
    Gets rid of unnecessary data fields listed in "delete_keys". '''
    


def format_date(date_str):
    ''' Takes date string and converts to a date object, adding one
    day so that the sleep data from the previous night is aligned with 
    current day.
    '''
    date_formatted = datetime.strptime(date_str, '%Y-%m-%d')
    one_day_added = date_formatted + timedelta(days=1)
    return one_day_added.date()

def convert_seconds(total_seconds):
    str_time = time.strftime("%H:%M", time.gmtime(total_seconds))
    return str_time
    
    
def add_sleep_to_db():
    ''' Commit data to sleep database model.'''
    with open('new_result.json', 'r') as file:
        selected_data = json.loads(file.read(), object_hook=date_hook)
        for entry in (selected_data['sleep']):
            day = format_date(entry['summary_date'])
            if db.session.query(Sleep).filter_by(date=day).count() < 1:
                prev_night_data = Sleep(date = day,
                    id = id_dict[day],
                    sleep_score = entry['score_total'],
                    total_rem_sleep = convert_seconds(entry['rem']),
                    total_deep_sleep = convert_seconds(entry['deep']),
                    sleep_efficiency = entry['efficiency'],
                    restlessness = entry['restless'],
                    rem_score = entry['score_rem'],
                    deep_score = entry['score_deep'],
                    total_sleep = convert_seconds(entry['total']))
                db.session.add(prev_night_data)
        db.session.commit()

def setup_oura_data():
    ''' Executes all functions relating to sleep data, adding data 
    to databases. 
    '''
    pull_oura_data()
    convert_json_data()
    add_sleep_to_db()

