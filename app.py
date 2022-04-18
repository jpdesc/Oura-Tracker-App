import os
from io import BytesIO
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


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SECRET_KEY'] = 'random string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


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
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.Date)
  type = db.Column(db.String)
  soreness = db.Column(db.Integer)
  intensity = db.Column(db.Integer)
  filename = db.Column(db.String(50))
  data = db.Column(db.LargeBinary)
  workout_log = db.Column(db.String)


class JournalForm(FlaskForm):
  journal_entry = StringField('Notes:', validators=[DataRequired()], widget=TextArea(), render_kw={'cols':25, 'rows':4})
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
  workout_type = SelectField(choices=['Swim', 'Weights', 'Other'])
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
  events.append({'title':'Journal Log', 'date':submitted_log.date, 'id':submitted_log.id})

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
    
    journal_entry = wellness_form.journal_entry.data
    focus = wellness_form.focus.data
    mood = wellness_form.mood.data
    energy = wellness_form.energy.data
    wellness_info = Log(journal=journal_entry, focus=focus, mood=mood,\
      energy=energy, date=date, id=page_id)
    db.session.add(wellness_info)
    db.session.commit()
    update_log_events(wellness_info)
    return redirect(url_for('index', page_id=page_id))

  if workout_form.validate_on_submit():
    file = request.files[str(workout_form.file.name)]
    type = workout_form.workout_type.data
    if not type:
      type = workout_form.specify_other.data
    soreness = workout_form.soreness.data
    intensity = workout_form.intensity.data
    workout_log = workout_form.workout_log.data
    workout_info = Workout(data=file.read(), date=date, id=page_id,\
      filename=file.filename, type=type, soreness=soreness, 
      intensity=intensity, workout_log=workout_log)
    db.session.add(workout_info)
    db.session.commit()
    #TODO: Implement workout events.
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
    wellness_form = JournalForm(focus=log.focus, mood=log.mood, energy=log.energy, journal_entry=log.journal)
  else:
    wellness_form = JournalForm()
  if workout:
    workout_form = WorkoutForm(soreness=workout.soreness, intensity=workout.intensity,workout_type=workout.type, file=workout.data, workout_log=workout.workout_log)
  else:
    workout_form = WorkoutForm()
  if wellness_form.validate_on_submit():
    wellness_form.focus = wellness_form.focus.data
    wellness_form.mood = wellness_form.mood.data
    wellness_form.energy = wellness_form.energy.data
    wellness_form.journal_entry = wellness_form.journal_entry.data
    db.session.add(log)
    db.session.commit()
    return redirect(url_for('index', page_id = page_id))
  if workout_form.validate_on_submit():
    workout_form.soreness = workout_form.soreness.data
    workout_form.intensity = workout_form.intensity.data
    workout_form.workout_type = workout_form.workout_type.data
    workout_form.file = workout_form.file.data
    db.session.add(workout)
    db.session.commit()
    return redirect(url_for('index', page_id = page_id))
  return render_template('edit_post.html', wellness_form=wellness_form, workout_form=workout_form, sleep=sleep, page_id=page_id, readiness=readiness)

@app.route('/calendar', methods = ['GET','POST'])
def calendar():
  return render_template('calendar.html', events=events)

@app.route('/process', methods = ['POST'])
def process():
  ''' Used to process ajax call for calendar event clicks.
  Routes to the correct index page based on the page_id/dates. 
  Session['url'] gets used by ajax call in calendar.html
  to update URL concurrently.
  '''
  date_str = request.form.get('date_str')
  clicked_id = date_str_cal[date_str]
  session['url'] = None
  session['url'] = url_for('index', page_id = clicked_id)
  return redirect(session['url'])

@app.route('/download/<page_id>')
def download(page_id):
    workout = Workout.query.filter_by(id=page_id).first()
    return send_file(BytesIO(workout.data), attachment_filename=workout.filename, as_attachment = True)


if __name__ == '__main__':
  fetch_oura_data.setup_oura_data()
  create_cal_events()
  app.run(debug=True)