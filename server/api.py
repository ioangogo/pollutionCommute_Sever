from flask import request, Blueprint
from . import db
from .models import Recording
import json

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
    recordings = Recording.query.filter(bottomLat <= Recording.lat <= topLat, bottomLng <= Recording.lng <= topLng)
    for recording in recordings:
        data = {
            "lat":recording.lat,
            "lng":recording.lng,
            "pm25": recording.pm25,
            "datetime": recording.date_time}
        result.append(data)
    return json.dumps(result)