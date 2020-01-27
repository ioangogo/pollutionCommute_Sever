from flask import request, Blueprint
from . import db
from .models import Recording
import json

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/GetSensorInBounds', methods=['POST'])
def apiGetSensorInBounds():
    requestData = request.json
    topLat = requestData['top']['lat']
    topLng = requestData['top']['lng']
    bottomLat= requestData['bottom']['lat']
    bottomLng = requestData['bottom']['lng']
    recordingsInArea = Recording.query.filter(bottomLat <= Recording.lat <= topLat, bottomLng <= Recording.lng <= topLng)
    return json.dumps(recordingsInArea.__dict__)