from time import time
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property
from sqlalchemy import func, cast, Integer
import os
import time

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)

#TODO: Move secret key to .env and make a new one.
app.config['SECRET_KEY'] = 'iauye8uhO8UF28h28c8uwcp8387AFG283HDJK'
# password = os.getenv('POSTGRES_PASSWORD')
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"postgresql://jwa:doggo@127.0.0.1:5432/oura_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

tags = db.Table(
    'tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('log_id', db.Integer, db.ForeignKey('log.id'), primary_key=True))


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    tag = db.Column(db.String, unique=True)

    def __repr__(self):
        return f'{self.tag}'


class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    focus = db.Column(db.Integer)
    mood = db.Column(db.Integer)
    energy = db.Column(db.Integer)
    stress = db.Column(db.Integer)
    journal = db.Column(db.String)
    tags = db.relationship('Tag',
                           secondary=tags,
                           lazy='subquery',
                           backref=db.backref('logs', lazy=True))


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
    food_cutoff = db.Column(db.Float)
    seconds_sleep = db.Column(db.Integer)

    # @hybrid_property
    # def datetime(self):
    #     return time.mktime(self.datetime_sleep.timetuple())

    # @datetime.expression
    # def datetime(cls):
    #     seconds = time.mktime(cls.datetime_sleep.timetuple())
    #     return seconds


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
    grade = db.Column(db.Integer)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    workout_log = db.Column(db.String)


class Weights(db.Model):
    __tablename__ = 'weights'
    id = db.Column(db.Integer, primary_key=True)
    exercises = db.Column(db.ARRAY(db.String))
    set_ranges = db.Column(db.ARRAY(db.String))
    reps = db.Column(db.ARRAY(db.String))
    weight = db.Column(db.ARRAY(db.String))
    subbed = db.Column(db.String)
    workout_id = db.Column(db.Integer)
    workout_week = db.Column(db.Integer)
    template_id = db.Column(db.Integer, db.ForeignKey("template.id"))


class Template(db.Model):
    __tablename__ = 'template'
    id = db.Column(db.Integer, primary_key=True)
    start_id = db.Column(db.Integer)
    template_name = db.Column(db.String)
    num_days = db.Column(db.Integer)
    row_nums = db.Column(db.ARRAY(db.Integer))
    num_excs = db.Column(db.ARRAY(db.Integer))
    weights = db.relationship('Weights', backref='template')
