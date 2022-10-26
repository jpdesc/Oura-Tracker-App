from ouraapp.extensions import db


class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    day_id = db.Column(db.Integer)
    date = db.Column(db.Date)
    title = db.Column(db.String)
    score = db.Column(db.Float)
    event = db.Column(db.JSON)
    subclass = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
