
from google.oauth2 import service_account
from googleapiclient.discovery import build
import string
import re
import json
import app



SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'
# creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
SPREADSHEET_ID = '1AdnxSengjtM0zwTgG7NtX1nBUdK0w4-368n8852WNPs'
sheet_prefix = 'meetPrep!'

# Dictionaries with key as the id number and value as row/column/number of exercises.
weeks_column = {}
workout_row = {1:6, 2:20, 3:31, 4:45}
exercises_by_workout = {1:9, 2:6, 3:9, 4:8}

alphabet_string = string.ascii_uppercase
alphabet_list = list(alphabet_string[3:])

# Create a dict with the google sheets column letter for each week.
for i, letter in enumerate(alphabet_list):
    weeks_column[i+1] = letter

def parse_reps_weight(reps_weight):
    ''' Separates reps and weight into two separate fields.
    For instance, 8x45 becomes reps=8 and weight=45.
    '''
    reps_list, weights_list = [], []
    subbed_list = ['' for x in range(len(reps_weight))]
    for i, input in enumerate(reps_weight):
        if input == '':
            reps_weight[i] = ''
        try:
            parsed_output = input[0].split('x')
        except IndexError:
            parsed_output = ''
        if len(parsed_output) == 2:
            reps = parsed_output[0]
            weight = parsed_output[1]
            if weight[-2:] == '**':
                weight = weight[:-2]
                subbed_list[i] = '**'
            elif weight[-1] == '*':
                weight = weight[:-1]
                subbed_list[i] = '*'
        else:
            reps = ''
            try:
                weight = input[0]
            except IndexError:
                weight = ''

        reps_list.append(reps)
        weights_list.append(weight)
        
    return reps_list, weights_list, subbed_list

def format_output(raw_output):
    '''Format google sheets data such that it is a plain string 
    without quotes or brackets.
    '''
    formatted_list = re.findall(r"[^\[\]\'\"]", raw_output)
    formatted_str = ''.join(formatted_list)
    return formatted_str

def init_sheets_api(range_names):
    service = build('sheets', 'v4', credentials=creds)
        # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().batchGet(spreadsheetId=SPREADSHEET_ID,\
            ranges=range_names).execute()
    return result

def subs(workout_data):
    ''' Substitutes up to two exercises per workout.If an 
    exercise field ends with * or **, that exercise will be 
    replaced. Returns the workout data with substitutions made.
    '''
    exercises = workout_data[0]
    substitutions = workout_data[4]
    subbed = workout_data[5]
    if substitutions:
        for i in range(len(workout_data[0])):
            try:
                first_substitution = (subbed[i] == '*')
                second_substitution = (subbed[i] == '**')
            except IndexError:
                pass
            if first_substitution:
                exercises[i] = substitutions[0]
            elif second_substitution:
                exercises[i] = substitutions[1]
    return workout_data[:-2]



def get_weights_data(workout_id, workout_week, id):
    ''' Formats the exercise data from google sheet based on 
    the workout id and week id of the Workout database object.
    '''
    row = workout_row.get(workout_id)
    col = weeks_column.get(workout_week)
    total_exercises = exercises_by_workout.get(workout_id)
    
    subs_row = row + total_exercises + 1
    
    range_names = [f"{sheet_prefix}A{row}:A{row + total_exercises}",
    f"{sheet_prefix}B{row}:B{row + total_exercises}",
    f"{sheet_prefix}{col}{row}:{col}{row + total_exercises}",
    f"{sheet_prefix}{col}{subs_row}:{col}{subs_row+2}"]
    sheets_data = init_sheets_api(range_names)
    ranges = sheets_data.get('valueRanges', [])
    exercises = ranges[0].get('values')
    set_ranges = ranges[1].get('values')
    reps_weight = ranges[2].get('values')
    substitutions = ranges[3].get('values')
    reps, weight, subbed = parse_reps_weight(reps_weight)
    
    for i in range(len(exercises)):
        exercises[i] = format_output(str(exercises[i]))
        try:
            set_ranges[i] = str(format_output(str(set_ranges[i])))
        except IndexError:
            pass
    if substitutions:
        for i in range(len(substitutions)):
            substitutions[i] = format_output(str(substitutions[i]))
    parsed_data = exercises, set_ranges, reps, weight, substitutions, subbed
    subs_made = subs(parsed_data)
    app.add_weights_to_db(subs_made, id, workout_id, workout_week)
    



def check_improvement(this_week, last_week):
    reps_improvement, weight_improvement = [], []
    for i, exercise in enumerate(this_week.exercises):
        reps_improved = False
        weight_improved = False
        check_empty_reps = (this_week.reps[i] and last_week.reps[i]) != ''
        check_empty_weights = (this_week.reps[i] and last_week.reps[i]) != ''
        if exercise == last_week.exercises[i] and check_empty_reps:
            reps_check = int(this_week.reps[i]) > int(last_week.reps[i]) and int(this_week.weight[i]) >= int(last_week.weight[i])
            if reps_check:
                reps_improved = True
        if exercise == last_week.exercises[i] and check_empty_weights:
            weights_check = float(this_week.weight[i]) > float(last_week.weight[i])
            if weights_check:
                weight_improved = True
        reps_improvement.append(reps_improved)
        weight_improvement.append(weight_improved)
    return reps_improvement, weight_improvement



