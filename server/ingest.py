from flask import request, Blueprint

bp = Blueprint('ingest', __name__, url_prefix='/ingest')

@bp.route('/ttnIn', methods=['POST'])
def ttnIn():
    if request.method == 'POST':
        data = request.json
        print(data)
        return data

