from flask_login import UserMixin
from . import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    EUI = db.Column(db.String(80), unique=True, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))

class Recording(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    pm25 = db.Column(db.Float)
    dB = db.Column(db.Float)
    sensor = db.Column(db.Integer, db.ForeignKey('sensor.id'))
