from flask import Flask
from flask_socketio import SocketIO
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from os import path
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
skt = SocketIO()
migrate = Migrate()
jwt = JWTManager()

DB_NAME = 'app.db'
UPLOAD_FOLDER = 'uploads'  
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}



def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)
    skt.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    CORS(app)
    
    from .auth.routes import authbp
    from .groups.routes import groupsbp

    app.register_blueprint(authbp)
    app.register_blueprint(groupsbp)

    
    create_database(app)
    
    return app

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_database(app):
    if not path.exists('app/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Database created!')
