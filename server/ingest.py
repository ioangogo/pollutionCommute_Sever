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
@bp.route('/ttnIn', methods=['POST', 'GET'])
def ttnIn():
    if request.method == 'POST':
        data = request.json
        deviceEUI = data['hardware_serial']
        nonce = data['payload_fields']['nonce']
        sensor = Sensor.query.filter_by(sensorEUI=deviceEUI).first()
        nonceCheck = Recording.query.filter_by(sensor=sensor, nonce=nonce, Recording.date_time.after(datetime.datetime.now - datetime.timedelta(days=1)))
        if sensor is not None:
            deviceID = sensor.id
            date = dateutil.parser.isoparse(data['metadata']['time'])
            lat = data['payload_fields']['lat']
            lng = data['payload_fields']['lng']
            pm25 = data['payload_fields']['pm25']
            newRecord = Recording(lat=lat, lng=lng, date_time=date, sensor=deviceID, pm25=pm25)
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
        timestamp = datetime.utcfromtimestamp(int(data['time']))
        nonce = data['data']['nonce']
        nonceCheck = Recording.query.filter_by(sensor=sensor, nonce=nonce, Recording.date_time.after(datetime.datetime.now - datetime.timedelta(days=1)))
        if(len(nonceCheck) is 0):
            lat = data['data']['lat']
            lng = data['data']['lng']
            pm25 = data['dara']['pm25']
            Recording(lat=lat, lng=lng, date_time=date, sensor=deviceEUI, pm25=pm25, nonce=nonce)
        else:
            print("Recording already recived")
            
