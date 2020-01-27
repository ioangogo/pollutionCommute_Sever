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
        sensor = Sensor.query.filter_by(sensorEUI=deviceEUI).first()
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