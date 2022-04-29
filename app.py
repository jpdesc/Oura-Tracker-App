from io import BytesIO
import os
from flask import Flask, render_template, session, redirect, url_for, request, send_file, jsonify, make_response
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, FileField, BooleanField, SelectField, FormField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, InputRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import date, timedelta, datetime
import fetch_oura_data
import json
from weights_data import get_weights_data


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SECRET_KEY'] = 'random string' #TODO: Change to actual password.
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://@localhost:5432/oura_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# jpdesc:{POSTGRES_PASSWORD}

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)

class Log(db.Model):
  __tablename__ = 'log'

  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.Date)
  focus = db.Column(db.Integer)
  mood = db.Column(db.Integer)
  energy = db.Column(db.Integer)
  journal = db.Column(db.String)
  
class Sleep(db.Model):
  __tablename__ = 'sleep'

  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.Date)
  sleep_score = db.Column(db.Integer)
  total_rem_sleep = db.Column(db.String)
  total_deep_sleep = db.Column(db.String)
  sleep_efficiency = db.Column(db.Integer)
  restlessness = db.Column(db.Integer)
  rem_score = db.Column(db.Integer)
  deep_score = db.Column(db.Integer)
  total_sleep = db.Column(db.String)

class Readiness(db.Model):
  __tablename__ = 'readiness'

  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.Date)
  readiness_score = db.Column(db.Integer)
  hrv_balance = db.Column(db.Integer)
  recovery_index = db.Column(db.Integer)
  resting_hr = db.Column(db.Integer)
  temperature = db.Column(db.Integer)
  
class Workout(db.Model):
  __tablename__ = 'workout'
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.Date)
  type = db.Column(db.String)
  soreness = db.Column(db.Integer)
  intensity = db.Column(db.Integer)
  filename = db.Column(db.String(50))
  data = db.Column(db.LargeBinary)
  workout_log = db.Column(db.String)
  

class Weights(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  exercises = db.Column(db.ARRAY(db.String))
  set_ranges = db.Column(db.ARRAY(db.String))
  reps = db.Column(db.ARRAY(db.String))
  weight = db.Column(db.ARRAY(db.String))
  subbed = db.Column(db.String)
  workout_id = db.Column(db.Integer)
  workout_week = db.Column(db.Integer)


class JournalForm(FlaskForm):
  journal = StringField('Notes:', validators=[DataRequired()], widget=TextArea(), render_kw={'cols':25, 'rows':4})
  focus = RadioField('Focus: ',
          choices=['1', '2', '3', '4', '5'], 
          validators=[InputRequired()])
  mood = RadioField('Mood: ',
          choices=['1', '2', '3', '4', '5'],
          validators=[InputRequired()])
  energy = RadioField('Energy: ',
          choices=['1', '2', '3', '4', '5'],
          validators=[InputRequired()])
  submit1 = SubmitField("Submit Wellness")

class WorkoutForm(FlaskForm):
  soreness = RadioField('Soreness:',
          choices=['1', '2', '3', '4', '5'])
  workout = BooleanField("Did you work out today?")
  intensity = RadioField('Workout Intensity:',
          choices=['1', '2', '3', '4', '5'])
  type = SelectField(choices=['Swim', 'Weights', 'Other'])
  specify_other = StringField("Specify other: ")
  file = FileField('Upload Workout File:')
  workout_log = StringField('Workout Notes:', widget=TextArea(), render_kw={'cols':25, 'rows':4})
  submit2 = SubmitField("Submit Workout")
  

id_dict = {}
events = []
date_str_cal = {}
today = date.today()

def format_date(date_str):
  formatted_date = date.strptime(date_str, "%Y-%m-%d")
  return formatted_date

def get_date(page_id, id_dict):
  for key, value in id_dict.items():
    if value == page_id:
      return key

def create_cal_events():
  sleep_query = Sleep.query.order_by(Sleep.id).all()
  for sleep in sleep_query:
    events.append({'title':'Sleep', 'date':sleep.date, 'id':sleep.id})

  log_query = Log.query.order_by(Log.id).all()
  for log in log_query:
    events.append({'title':'Wellness Log', 'date':log.date, 'id':log.id})

  workout_query = Workout.query.order_by(Workout.id).all()
  for workout in workout_query:
    events.append({'title':workout.type, 'date':workout.date, 'id':workout.id})

def update_log_events(submitted_log):
  events.append({'title':'Wellness Log', 'date':submitted_log.date, 'id':submitted_log.id})
  
def update_workout_events(submitted_log, type):
  events.append({'title': type, 'date':submitted_log.date, 'id':submitted_log.id})

def get_workout_week_num():
  last_workout = Weights.query.order_by(Weights.id.desc()).first()
  if last_workout.workout_id == 4:
    week = last_workout.workout_week + 1
  else:
    week = last_workout.workout_week
  return week

def get_workout_id():
  last_workout = Weights.query.order_by(Weights.id.desc()).first()
  if last_workout.workout_id == 4:
    workout_id = 1
  else:
    workout_id = last_workout.workout_id + 1
  return workout_id

def add_weights_to_db(subs_made, id, workout_id, workout_week):
    db_dict = {}
    for i, val in enumerate(subs_made):
        db_dict[i] = val
    # weight = Weights.query.filter_by(id = id).first()
    # weight.exercises = db_dict[0]
    # weight.set_ranges = db_dict[1]
    # weight.reps = db_dict[2]
    # weight.weight = db_dict[3]
    weights_info = Weights(id=id, exercises = db_dict[0], set_ranges = db_dict[1],\
      reps = db_dict[2], weight = db_dict[3], workout_week = workout_week, workout_id=workout_id)
    db.session.add(weights_info)
    db.session.commit()

def check_improvement(this_week, last_week):
  reps_improvement, weight_improvement = [], []
  for i, exercise in enumerate(this_week.exercises):
    reps_improved = False
    weight_improved = False
    check_empty_reps = (this_week.reps[i] and last_week.reps[i]) != ''
    check_empty_weight = (this_week.reps[i] and last_week.reps[i]) != ''
    exercises_match = exercise == last_week.exercises[i]
    if exercises_match and check_empty_reps:
      reps_check = int(this_week.reps[i]) > int(last_week.reps[i]) and int(this_week.weight[i]) >= int(last_week.weight[i])
      if reps_check:
        reps_improved = True
    if exercises_match and check_empty_weight:
      weight_check = float(this_week.weight[i]) > float(last_week.weight[i])
      if weight_check:
        weight_improved = True
    reps_improvement.append(reps_improved)
    weight_improvement.append(weight_improved)
  return reps_improvement, weight_improvement

all_days = [date(2022, 1, 1) + timedelta(days=x) for x in range((today - date(2022, 1, 1)).days + 5)]
for i, day in enumerate(all_days):
  id_dict[day] = i
  date_str_cal[str(day)] = id_dict[day]

@app.route('/', defaults={'page_id': id_dict[today]}, methods=['GET', 'POST'])
@app.route('/<int:page_id>', methods=['GET', 'POST'])
def index(page_id):
  date = get_date(page_id, id_dict)
  wellness_form = JournalForm()
  workout_form = WorkoutForm()
  sleep = Sleep.query.filter(Sleep.id == page_id).first()
  log = Log.query.filter(Log.id == page_id).first()

  readiness = Readiness.query.filter(Readiness.id == page_id).first()
  workout = Workout.query.filter(Workout.id == page_id).first()
    
  if wellness_form.validate_on_submit():
    
    journal = wellness_form.journal.data
    focus = wellness_form.focus.data
    mood = wellness_form.mood.data
    energy = wellness_form.energy.data
    wellness_info = Log(journal=journal, focus=focus, mood=mood,\
      energy=energy, date=date, id=page_id)
    db.session.add(wellness_info)
    db.session.commit()
    update_log_events(wellness_info)
    return redirect(url_for('index', page_id=page_id))

  if workout_form.validate_on_submit():
    file = request.files[str(workout_form.file.name)]
    type = workout_form.type.data
    if type == "Other":
      type = workout_form.specify_other.data
    soreness = workout_form.soreness.data
    intensity = workout_form.intensity.data
    workout_log = workout_form.workout_log.data
    workout_info = Workout(data=file.read(), date=date, id=page_id,\
      filename=file.filename, type=type, soreness=soreness, 
      intensity=intensity, workout_log=workout_log)
    if type == "Weights":
      get_weights_data(get_workout_id(), get_workout_week_num(), page_id)
    db.session.add(workout_info)
    db.session.commit()
    update_workout_events(workout_info, type)
    return redirect(url_for('index', page_id=page_id))

  return render_template('index.html', 
    wellness_form = wellness_form,
    workout_form = workout_form,
    sleep = sleep,
    log = log,
    page_id = page_id,
    date = date,
    readiness = readiness,
    workout = workout)

@app.route('/edit/<int:page_id>', methods=['GET', 'POST'])
def edit_log(page_id):
  sleep = Sleep.query.get(page_id)
  readiness = Readiness.query.get(page_id)
  log = Log.query.get(page_id)
  workout = Workout.query.get(page_id)
  if log:
    wellness_form = JournalForm(focus=log.focus, mood=log.mood, energy=log.energy, journal=log.journal)
  else:
    wellness_form = JournalForm()
  if workout:
    workout_form = WorkoutForm(soreness=workout.soreness, intensity=workout.intensity,type=workout.type, specify_other= None, file=workout.data, workout_log=workout.workout_log)
  else:
    workout_form = WorkoutForm()
  if wellness_form.validate_on_submit():
    log.focus = wellness_form.focus.data
    log.mood = wellness_form.mood.data
    log.energy = wellness_form.energy.data
    log.journal = wellness_form.journal.data
    db.session.add(log)
    db.session.commit()
    return redirect(url_for('index', page_id = page_id))

  if workout_form.validate_on_submit():
    workout.soreness = workout_form.soreness.data
    workout.intensity = workout_form.intensity.data
    if workout.type == 'Other':
      workout.type = workout_form.specify_other.data
    else:
      workout.type = workout_form.type
    workout.file = workout_form.file.data
    db.session.add(workout)
    db.session.commit()
    return redirect(url_for('index', page_id = page_id))
  return render_template('edit_post.html', wellness_form=wellness_form, workout_form=workout_form, sleep=sleep, page_id=page_id, readiness=readiness)

@app.route('/calendar', methods = ['GET','POST'])
def calendar():
  session['url'] = url_for('index', page_id = None)
  return render_template('calendar.html', events=events)

@app.route('/process', methods = ['POST'])
def process():
  ''' Used to process ajax call for calendar event clicks.
  Routes to the correct index page based on the page_id/dates. 
  '''
  date_str = request.form.get('date_str')
  clicked_id = date_str_cal[date_str]
  return redirect(url_for('index', page_id = clicked_id))

@app.route('/download/<page_id>')
def download(page_id):
    workout = Workout.query.filter_by(id=page_id).first()
    return send_file(BytesIO(workout.data), attachment_filename=workout.filename, as_attachment = True)

@app.route('/weights/<page_id>')
def weights(page_id):
  this_week = Weights.query.filter_by(id=page_id).first()
  try:
    last_week = Weights.query.filter_by(workout_id=this_week.workout_id, workout_week=(this_week.workout_week - 1)).first()
    reps_improve, weight_improve = check_improvement(this_week, last_week)
  except(AttributeError):
    reps_improve, weight_improve = None, None


  return render_template('workout.html', page_id=page_id, weights=this_week, reps_improve = reps_improve, weight_improve = weight_improve)

if __name__ == '__main__':
  fetch_oura_data.setup_oura_data()
  create_cal_events()
  app.run(debug=True)