from .extensions import db


class Day(db.Model):
    __tablename__ = 'day'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    date = db.Column(db.Date, unique=True)
    date_str = db.Column(db.String, unique=True)
