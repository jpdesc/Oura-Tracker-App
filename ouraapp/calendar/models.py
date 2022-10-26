from ouraapp.extensions import db


class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    day_id = db.Column(db.Integer)
    title = db.Column(db.String)
    score = db.Column(db.Float)
    event = db.Column(db.JSON)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
