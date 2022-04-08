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

def format_date(date_str):
  formatted_date = date.strptime(date_str, "%Y-%m-%d")
  return formatted_date

id_dict = {}
events = []
today = date.today()

all_days = [date(2022, 1, 1) + timedelta(days=x) for x in range((today - date(2022, 1, 1)).days + 5)]
for i, day in enumerate(all_days):
  id_dict[day] = i

sleep_query = Sleep.query.order_by(Sleep.id).all()
for day in sleep_query:
  events.append({'title':'Sleep', 'date':day.date, 'id':day.id})

log_query = Log.query.order_by(Log.id).all()
for day in log_query:
  events.append({'title':'Journal Log', 'date':day.date, 'id':day.id})

@app.route('/', defaults={'page_id': id_dict[today]}, methods=['GET', 'POST'])
@app.route('/<int:page_id>', methods=['GET', 'POST'])
def index(page_id):
  journal_entry = None
  focus = None
  mood = None
  energy = None

  form = JournalForm()
  
  try:
    sleep = Sleep.query.filter(Sleep.id == page_id).first()
  except:
    sleep = None
  try:
    log = Log.query.filter(Log.id == page_id).first()
  except:
    print("Log = None")
    log = None
    
  if form.validate_on_submit():
    journal_entry = form.journal_entry.data
    focus = form.focus.data
    mood = form.mood.data
    energy = form.energy.data
    day_info = Log(journal=journal_entry, focus=focus, mood=mood, energy=energy, date=today, id=page_id)
    db.session.add(day_info)
    db.session.commit()
    form.journal_entry.data = ''
  
  return render_template('index.html', 
    journal_entry = journal_entry,
    focus = focus, 
    mood = mood,
    energy = energy,
    form = form,
    page_id = page_id,
    sleep = sleep,
    log = log)

@app.route('/edit/<int:page_id>', methods=['GET', 'POST'])
def edit_log(page_id):
  
  sleep = Log.query.get_or_404(page_id)
  form = JournalForm()
  log = Log.query.get_or_404(page_id)
  if form.validate_on_submit():
    log.focus = form.focus.data
    log.mood = form.mood.data
    log.energy = form.energy.data
    log.journal = form.journal_entry.data
    db.session.add(log)
    db.session.commit()
    return redirect(url_for('/<page_id>'))
  form.focus.data = log.focus
  form.mood.data = log.mood
  form.energy.data = log.energy
  form.journal_entry.data = log.journal
  return render_template('edit_post.html', form=form, sleep=sleep, page_id=page_id)


@app.route('/calendar')
def calendar():
  return render_template('calendar.html', events=events)

if __name__ == '__main__':
  fetch_oura_data.setup_oura_data()
  app.run(debug=True)