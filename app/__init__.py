from flask import Flask
from flask_socketio import SocketIO
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from os import path

db = SQLAlchemy()
skt = SocketIO()
migrate = Migrate()

DB_NAME = 'app.db'

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    
    db.init_app(app)
    skt.init_app(app)
    migrate.init_app(app, db)
    
    CORS(app)
    
    from .auth.routes import authbp
    app.register_blueprint(authbp)
    
    create_database(app)
    
    return app

def create_database(app):
    if not path.exists('app/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Database created!')
