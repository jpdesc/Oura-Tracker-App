from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
import jwt
import os
from dotenv import load_dotenv
from pathlib import Path
from ouraapp.extensions import db

dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    oura_access_token = db.Column(db.String(50))
    join_date = db.Column(db.Date)
    tags = db.relationship('Tag', backref='user')
    logs = db.relationship('Log', backref='user')
    sleeps = db.relationship('Sleep', backref='user')
    readies = db.relationship('Readiness', backref='user')
    workouts = db.relationship('Workout', backref='user')
    weights = db.relationship('Weights', backref='user')
    templates = db.relationship('Template', backref='user')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {
                'reset_password': self.id,
                'exp': time() + expires_in
            },
            os.getenv('SECRET_KEY'),
            algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token,
                            os.getenv('SECRET_KEY'),
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
