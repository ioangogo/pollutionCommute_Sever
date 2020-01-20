from flask_login import UserMixin
from . import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    sensorNum = db.Column(db.Integer)

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    sensorEUI = db.Column(db.String(80), unique=True, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))

class Recording(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    pm25 = db.Column(db.Float)
    dB = db.Column(db.Float, default=0.0)
    date_time = db.Column(db.DateTime)
    sensor = db.Column(db.Integer, db.ForeignKey('sensor.id'))
