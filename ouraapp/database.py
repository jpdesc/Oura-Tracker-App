from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    tags = db.relationship('Tag', backref='user', lazy=True)
    logs = db.relationship('Log', backref='user', lazy=True)
    sleeps = db.relationship('Sleep', backref='user', lazy=True)
    readies = db.relationship('Readiness', backref='user', lazy=True)
    workouts = db.relationship('Workout', backref='user', lazy=True)
    weights = db.relationship('Weights', backref='user', lazy=True)
    templates = db.relationship('Template', backref='user', lazy=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


tags = db.Table(
    'tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('log_id', db.Integer, db.ForeignKey('log.id'), primary_key=True))


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    tag = db.Column(db.String, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Readiness(db.Model):
    __tablename__ = 'readiness'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    readiness_score = db.Column(db.Integer)
    hrv_balance = db.Column(db.Integer)
    recovery_index = db.Column(db.Integer)
    resting_hr = db.Column(db.Integer)
    temperature = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Template(db.Model):
    __tablename__ = 'template'
    id = db.Column(db.Integer, primary_key=True)
    start_id = db.Column(db.Integer)
    template_name = db.Column(db.String)
    num_days = db.Column(db.Integer)
    row_nums = db.Column(db.ARRAY(db.Integer))
    num_excs = db.Column(db.ARRAY(db.Integer))
    weights = db.relationship('Weights', backref='template')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    event = db.Column(db.JSON)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
