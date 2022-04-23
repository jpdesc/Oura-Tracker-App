
from google.oauth2 import service_account
from googleapiclient.discovery import build
import string
import re

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'
# creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
SPREADSHEET_ID = '1AdnxSengjtM0zwTgG7NtX1nBUdK0w4-368n8852WNPs'
sheet_prefix = 'meetPrep!'

weeks_column = {}
workout_row = {1:6, 2:17, 3:25, 4:36}
exercises_by_workout = {1:10, 2:6, 3:9, 4:8}
parsed_data = []

alphabet_string = string.ascii_uppercase
alphabet_list = list(alphabet_string[3:])

# Create a dict with the google sheets column letter for each week.
for i, letter in enumerate(alphabet_list):
    weeks_column[i+1] = letter

def parse_reps_weight(reps_weight):
    reps_list = []
    weights_list = []
    for input in reps_weight:
        try:
            parsed_output = input[0].split('x')
        except IndexError:
            parsed_output = ''

        print(parsed_output)
        if len(parsed_output) > 1:
            reps = parsed_output[0]
            weight = parsed_output[1]
            # print(reps, weight)
        else:
            reps = ''
            try:
                weight = input[0]
            except IndexError:
                weight = ''
        reps_list.append(reps)
        weights_list.append(weight)
    return reps_list, weights_list

def format_output(raw_output):
   
    formatted_list = re.findall(r'[^\[\]\'\"]', raw_output)
    formatted_str = ''.join(formatted_list)
    return formatted_str
    

def get_weights_data(workout_id, workout_week):
    row = workout_row.get(workout_id)
    col = weeks_column.get(workout_week)
    total_exercises = exercises_by_workout.get(workout_id)
    range_names = [f"{sheet_prefix}A{row}:A{row + total_exercises}",
    f"{sheet_prefix}B{row}:B{row + total_exercises}",
    f"{sheet_prefix}{col}{row}:{col}{row + total_exercises}"]
    service = build('sheets', 'v4', credentials=creds)
        # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().batchGet(spreadsheetId=SPREADSHEET_ID,\
            ranges=range_names).execute()
    ranges = result.get('valueRanges', [])
    exercises = ranges[0].get('values')
    set_ranges = ranges[1].get('values')
    reps_weight = ranges[2].get('values')
    reps, weight = parse_reps_weight(reps_weight)
    for i in range(len(exercises)):
        exercises[i] = format_output(str(exercises[i]))
    for i in range(len(set_ranges)):
        set_ranges[i] = format_output(str(set_ranges[i]))
    parsed_data = exercises, set_ranges, reps, weight
    return parsed_data


    
    