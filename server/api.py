from flask import request, Blueprint
from . import db
from .models import Recording

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/apiGetSensorInBounds', methods=['POST'])
def apiGetSensorInBounds():
    requestData = request.json
    topLat = requestData['mapBound'][0][0]
    topLng = requestData['mapBound'][0][1]
    bottomLat= requestData['mapBound'][1][0]
    bottomLng = requestData['mapBound'][1][1]
    recordingsInArea = Recording.query.filter(bottomLat <= Recording.lat <= topLat, bottomLng <= Recording.lng <= topLng)