from flask import request, Blueprint
from .models import Sensor, Recording, User
import datetime
from . import db

bp = Blueprint('ingest', __name__, url_prefix='/ingest')

# Function: ttnIn
# Decription: this route handles incoming data from the things network
#
#
@bp.route('/ttnIn', methods=['POST'])
def ttnIn():
    if request.method == 'POST':
        data = request.json
        print(data)
        return data

@bp.route('/sensorIn', methods=['POST'])
def sensorIn():
    if request.method == 'POST':
        data = request.json
        deviceID = data['hardware_serial']
        date = datetime.datetime.fromisoformat(data['metadata']['gateways'][0]['time'])
        lat = data['payload_fields']['lat']
        lng = data['payload_fields']['lng']
        pm25 = data['payload_fields']['pm25']
        newRecord = Recording(lat=lat, lng=lng, date_time=date, sensor=deviceID, pm25=pm25)
        db.session.add(newRecord)
        print(data)
        return data