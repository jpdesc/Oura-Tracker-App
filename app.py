import os
from flask import Flask, render_template, session, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
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

  id = db.Column(db.Date, primary_key=True)
  focus = db.Column(db.Integer)
  mood = db.Column(db.Integer)
  energy = db.Column(db.Integer)
  journal = db.Column(db.String)
  
class Sleep(db.Model):
  __tablename__ = 'sleep'

  id = db.Column(db.Date, primary_key=True)
  sleep_score = db.Column(db.Integer)
  total_rem_sleep = db.Column(db.String)
  total_deep_sleep = db.Column(db.String)
  sleep_efficiency = db.Column(db.Integer)
  restlessness = db.Column(db.Integer)
  rem_score = db.Column(db.Integer)
  deep_score = db.Column(db.Integer)
  total_sleep = db.Column(db.String)
  

class JournalForm(FlaskForm):
  journal_entry = StringField("Notes: ", validators=[DataRequired()])
  focus = RadioField('Focus: ',
          choices=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
          validators=[InputRequired()])
  mood = RadioField('Mood: ',
          choices=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
          validators=[InputRequired()])
  energy = RadioField('Energy: ',
          choices=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
          validators=[InputRequired()])
  submit = SubmitField("Submit")


events = []

sleep_query = Sleep.query.order_by(Sleep.id).all()
for day in sleep_query:
  events.append({'title':'Sleep', 'date':day.id})

log_query = Log.query.order_by(Log.id).all()
for day in log_query:
  events.append({'title':'Journal Log', 'date':day.id})


@app.route('/', methods=['GET', 'POST'])
def index():
  journal_entry = None
  focus = None
  mood = None
  energy = None

  if request.args.get('cal_date'):
    selected_date = request.args.get('cal_date')
  else:
    selected_date = date.today()
    
  form = JournalForm()
  try:
    sleep = Sleep.query.filter(Sleep.id == selected_date).first()
    print(sleep)
  except:
    print("Sleep = None")
    sleep = None
  try:
    log = Log.query.filter(Log.id == selected_date).first()
  except:
    print("Log = None")
    log = None
  if form.validate_on_submit():
    journal_entry = form.journal_entry.data
    focus = form.focus.data
    mood = form.mood.data
    energy = form.energy.data
    day_info = Log(journal=journal_entry, focus=focus, mood=mood, energy=energy, id=date.today())
    db.session.add(day_info)
    db.session.commit()
    form.journal_entry.data = ''
  
  cal_date = None
  return render_template('index.html', 
    journal_entry = journal_entry,
    focus = focus, 
    mood = mood,
    energy = energy,
    form = form,
    selected_date = selected_date,
    sleep = sleep,
    log = log)
 
@app.route('/calendar')
def calendar():
  return render_template('calendar.html', events=events)

if __name__ == '__main__':
  fetch_oura_data.setup_oura_data()
  app.run(debug=True)