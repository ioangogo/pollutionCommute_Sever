from flask import request, Blueprint
from . import db

bp = Blueprint('api', __name__, url_prefix='/api')