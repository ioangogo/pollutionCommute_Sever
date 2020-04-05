from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from flask_table import Table, Col, ButtonCol, LinkCol
from datetime import datetime, timedelta
import binascii
import ttn
from .util.ttndevice import genNewDevice
from . import db
from .models import Sensor, Recording
from .secrets import TTN_app_ID, TTN_app_key

ttnClient = ttn.ApplicationClient(TTN_app_ID, TTN_app_key)

bp = Blueprint('views', __name__,)

class sensorRecordTable(Table):
    date_time = Col("Time Of Recording")
    lat = lat = Col("Lat")
    lng = Col("Lng")
    pm25 = Col("PM 2.5")

class sensorTable(Table):
    name = Col("Sensor ID")
    sensorEUI = Col("Sensor EUI")
    veiw_records_col = LinkCol("View Data", 'views.sensorRecords', url_kwargs=dict(sensor_id = "sensorEUI"))
    deleteSensorCol = ButtonCol("Delete Sensor", 'views.deleteSensor', url_kwargs=dict(name = "name"))

@bp.route('/map')
def map():
    return render_template("map.html")

@bp.route('/')
def index():
    return render_template("index.html")

@bp.route('/setupGuide')
def index():
    return render_template("guide.html")

@bp.route('/sensors')
@login_required
def sensors():
    sensors = Sensor.query.filter_by(owner=current_user.id)
    table = sensorTable(items=sensors)
    return render_template("sensors.html", sensor_table=table)

@bp.route('/sensors/<sensor_id>')
@login_required
def sensorRecords(sensor_id):
    sensor = Sensor.query.filter_by(sensorEUI=sensor_id).first()
    if current_user.id == sensor.owner:
        recordings=Recording.query.filter(Recording.date_time.between(datetime.now(), datetime.now() - timedelta(days=7)), Recording.sensor == sensor.id)
        table = sensorRecordTable(recordings)
        return render_template("sensorrecord.html", sensor_table=table, sensor_id=sensor_id)
    else:
        return redirect(url_for('views.sensors'))

@bp.route('/deleteSensor',methods=['POST'])
@login_required
def deleteSensor():
    if request.method == 'POST':
        print(request.args)
        sensor_name = request.args.get("name")
        delsensor = Sensor.query.filter_by(name=sensor_name).first()
        db.session.delete(delsensor)
        db.session.commit()
        ttnClient.delete_device(request.args.get("name"))
        
    return redirect(url_for('views.sensors'))


@bp.route('/sensorOnboard', methods=['GET'])
@login_required
def sensorsOnboard():
    if request.method == 'GET':
        error = None
        lastid = current_user.sensorNum
        if lastid is None:
            lastid = 0
        newid = lastid+1
        newdevice = genNewDevice(current_user.username, newid)
        print(newdevice)
        ttnClient.register_device(newdevice["description"], newdevice)
        newSensor = Sensor(name=newdevice["description"], sensorEUI=newdevice["devEui"].decode(),
        owner=current_user.id)
        current_user.sensorNum = newid
        db.session.add(newSensor)
        db.session.commit()
        sensorInfo = [newdevice["devEui"].decode(), newdevice["appKey"].decode()]
        return render_template("sensoronboarding.html", sensorInfo=sensorInfo)


