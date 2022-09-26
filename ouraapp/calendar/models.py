from ouraapp.extensions import db


class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    event = db.Column(db.JSON)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
