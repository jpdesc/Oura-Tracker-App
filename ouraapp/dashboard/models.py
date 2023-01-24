from ouraapp.extensions import db

tags = db.Table(
    'tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('log_id', db.Integer, db.ForeignKey('log.id'), primary_key=True))


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    day_id = db.Column(db.Integer)
    tag = db.Column(db.String, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'{self.tag}'


class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    day_id = db.Column(db.Integer)
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
    id = db.Column(db.Integer, primary_key=True, unique=True)
    day_id = db.Column(db.Integer)
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
    id = db.Column(db.Integer, primary_key=True, unique=True)
    day_id = db.Column(db.Integer)
    date = db.Column(db.Date)
    readiness_score = db.Column(db.Integer)
    hrv_balance = db.Column(db.Integer)
    recovery_index = db.Column(db.Integer)
    resting_hr = db.Column(db.Integer)
    temperature = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Workout(db.Model):
    __tablename__ = 'workout'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    day_id = db.Column(db.Integer)
    date = db.Column(db.Date)
    type = db.Column(db.String)
    soreness = db.Column(db.Integer)
    grade = db.Column(db.Integer)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    weights_data = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
