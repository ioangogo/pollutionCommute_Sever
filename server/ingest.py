from flask import request, Blueprint, logging
from .models import Sensor, Recording, User
import datetime
import dateutil.parser
from . import db, app

bp = Blueprint('ingest', __name__, url_prefix='/ingest')

# Function: ttnIn
# Decription: this route handles incoming data from the things network
#
#


def packetCheck(data, deviceEUI, packetTime):
    nonceValid = False
    sensor = Sensor.query.filter_by(sensorEUI=deviceEUI).first()
    if "nonce" in data.keys():
        nonce = data['nonce']
        # I dont entirely have confidence in the ESP32's random number genrator so i only check if the nonce has been used in the past day
        nonceCheck = Recording.query.filter(Recording.date_time.between(packetTime - datetime.timedelta(days=7), packetTime), Recording.sensor == sensor.id, Recording.nonce == nonce)

        if nonceCheck.first() is None:
            nonceValid = True
        elif nonceCheck.first() == 0:
            nonceValid = True
        else:
            nonceValid = False
    else:
        nonceValid = True
    if sensor is not None and nonceValid:
        app.logger.info("The packet is unique")
        print(nonceCheck.first())
        return (sensor, True)
    else:
        app.logger.warning("The packet has been seen in the past week")
        print(nonceCheck.first())
        return (sensor, False)


@bp.route('/ttnIn', methods=['POST', 'GET'])
def ttnIn():
    if request.method == 'POST':
        data = request.json
        deviceEUI = data['hardware_serial']
        date = dateutil.parser.isoparse(data['metadata']['time'])
        sensor, packetValid = packetCheck(data['payload_fields'], deviceEUI, date)
        if packetValid:
            deviceID = sensor.id
            date = dateutil.parser.isoparse(data['metadata']['time'])
            lat = data['payload_fields']['lat']
            lng = data['payload_fields']['lng']
            pm25 = data['payload_fields']['pm25']
            nonce = data['payload_fields']['nonce']
            newRecord = Recording(lat=lat, lng=lng, date_time=date, sensor=sensor.id, pm25=pm25, nonce=nonce)
            db.session.add(newRecord)
            db.session.commit()
            return data
        else:
            return "Invalid Device"
    if request.method == 'GET':
        return "This Endpoint Is not for Human Use"

@bp.route('/sensorIn', methods=['POST', 'GET'])
def sensorIn():
    if request.method == 'GET':
        return "This Endpoint Is not for Human Use"
    elif request.method == 'POST':
        data = request.json
        deviceEUI = data['sensor']
        sensor = Sensor.query.filter_by(sensorEUI=deviceEUI).first()
        timestamp = datetime.datetime.utcfromtimestamp(int(data['time']))
        sensor, packetValid = packetCheck(data['data'], deviceEUI, timestamp)
        if packetValid:
            nonce = data['data']['nonce']
            lat = data['data']['lat']
            lng = data['data']['lng']
            pm25 = data['data']['pm25']
            newRecord = Recording(lat=lat, lng=lng, date_time=timestamp, sensor=sensor.id, pm25=pm25, nonce=nonce)
            db.session.add(newRecord)
            db.session.commit()
            return data
        else:
            return "Recording already recived"
            
