from flask import request, Blueprint
from .models import Sensor, Recording, User
import datetime
import dateutil.parser
from . import db

bp = Blueprint('ingest', __name__, url_prefix='/ingest')

# Function: ttnIn
# Decription: this route handles incoming data from the things network
#
#


def packetCheck(json, deviceEUI):
    nonceValid = False
    sensor = Sensor.query.filter_by(sensorEUI=deviceEUI).first()
    if "nonce" in data['payload_fields'].keys():
        nonce = data['payload_fields']['nonce']
        # I dont entirely have confidence in the ESP32's random number genrator so i only check if the nonce has been used in the past day
        nonceCheck = Recording.query.filter_by(Recording.date_time.after(datetime.datetime.now - datetime.timedelta(days=1)), sensor=sensor, nonce=nonce)
        if len(nonceCheck) == 0:
            nonceValid = True
        elif nonceCheck.first() == "":
            nonceValid = True
    else:
        nonceValid = True
    
    if sensor is not None and nonceValid:
        return (sensor, True)
    else:
        return (sensor, False)


@bp.route('/ttnIn', methods=['POST', 'GET'])
def ttnIn():
    if request.method == 'POST':
        print(data)
        data = request.json
        deviceEUI = data['hardware_serial']
        sensor, packetValid = packetCheck(data, deviceEUI)
        if packetValid:
            deviceID = sensor.id
            date = dateutil.parser.isoparse(data['metadata']['time'])
            lat = data['payload_fields']['lat']
            lng = data['payload_fields']['lng']
            pm25 = data['payload_fields']['pm25']
            nonce = data['payload_fields']['nonce']
            newRecord = Recording(lat=lat, lng=lng, date_time=date, sensor=deviceEUI, pm25=pm25, nonce=nonce)
            db.session.add(newRecord)
            db.session.commit()
            print(data)
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
        sensor, packetValid = packetCheck(data, deviceEUI)
        if packetValid:
            nonce = data['data']['nonce']
            lat = data['data']['lat']
            lng = data['data']['lng']
            pm25 = data['dara']['pm25']
            Recording(lat=lat, lng=lng, date_time=timestamp, sensor=deviceEUI, pm25=pm25, nonce=nonce)
        else:
            print("Recording already recived")
            
