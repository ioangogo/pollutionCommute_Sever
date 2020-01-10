from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
import ttn
from .util.ttndevice import genNewDevice
from . import db
from .models import Sensor

ttnClient = ttn.ApplicationClient("ioan_pol_sensor", TTN_app_ID)

bp = Blueprint('views', __name__,)

@bp.route('/map')
def map():
    return 'map'

@bp.route('/')
def index():
    return render_template("index.html")

@bp.route('/sensors')
@login_required
def sensors():
    return 'sensors'

@bp.route('/sensorOnboard', methods=['GET', 'POST'])
@login_required
def sensorsOnboard():
    if request.method == 'POST':
        error = None
        try:
            lastid = Sensor.query.filter_by(..).order_by(sqlalchemy.desc(Sensor.id)).first().id
            if lastid == None:
                newid = 0
            else:
                newid = lastid+1
            newdevice = genNewDevice(current_user.username, newid)
            ttnClient.register_device(newdevice["description"],newdevice)
        except RuntimeError as e:
            error = e
        return redirect(url_for("views.sensors"))


