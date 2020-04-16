from flask import request, Blueprint
from . import db
from .models import Recording
import json
import datetime, dateutil

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/GetSensorInBounds', methods=['POST'])
def apiGetSensorInBounds():
    requestData = request.json
    result=[]
    print(requestData)
    topLat = requestData['top']['lat']
    topLng = requestData['top']['lng']
    bottomLat= requestData['bottom']['lat']
    bottomLng = requestData['bottom']['lng']
    recordings = Recording.query.filter(Recording.lat.between(topLat,bottomLat), Recording.lng.between(topLng, bottomLng))
    for recording in recordings:
        print(recording)
        data = {
            "lat":recording.lat,
            "lng":recording.lng,
            "pm25": recording.pm25,
            "datetime": recording.date_time.isoformat()
            }
        result.append(data)
    print(result)
    return json.dumps(result)

@bp.route('/GetSensorInTimeBounds', methods=['POST'])
def apiGetSensorInTimeBounds():
    requestData = request.json
    result=[]
    print(requestData)
    topLat = requestData['top']['lat']
    topLng = requestData['top']['lng']
    bottomLat= requestData['bottom']['lat']
    bottomLng = requestData['bottom']['lng']
    before = None
    after = None
    if "before" in requestData:
        before = dateutil.parser(requestData["before"])
    else:
        before = datetime.datetime.now()
    
    if "after" in requestData:
        after = dateutil.parser(requestData["after"])
    else:
        after = datetime.datetime.utcfromtimestamp("0")
    
    recordings = Recording.query.filter(Recording.lat.between(topLat,bottomLat), Recording.lng.between(topLng, bottomLng), Recording.date_time.between(after, before))
    for recording in recordings:
        print(recording)
        data = {
            "lat":recording.lat,
            "lng":recording.lng,
            "pm25": recording.pm25,
            "datetime": recording.date_time.isoformat()
            }
        result.append(data)
    print(result)
    return json.dumps(result)