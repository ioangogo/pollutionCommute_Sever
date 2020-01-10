from flask import request, Blueprint
from .models import Sensor, Recording, User
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
        print(data)
        return data