import os
from pathlib import Path
from flask import Flask
from flask_login import LoginManager 
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

db = SQLAlchemy()   


def create_app(test_config=None):
    instancePath = os.path.join(str(Path.home()), ".commutePollution/")
    if not os.path.exists(instancePath):
        os.mkdir(instancePath)

    app = Flask(__name__, instance_path=instancePath)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    # create and configure the app
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///"+os.path.join(os.path.realpath(app.instance_path), 'server.sqlite'),
        SECRET_KEY = 'totallyInsecure',
        ENV = 'development'
    )
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.cfg', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    from . import veiws
    app.register_blueprint(veiws.bp)
    
    from . import auth
    app.register_blueprint(auth.auth)
    

    from . import ingest
    app.register_blueprint(ingest.bp)

    from . import api
    app.register_blueprint(api.bp)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    return app
