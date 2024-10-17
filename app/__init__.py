from flask import Flask
from flask_socketio import SocketIO
from .config import Config,TestingConfig
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from os import path
from flask_jwt_extended import JWTManager
from datetime import timedelta

# Initialize extensions
db = SQLAlchemy()
skt = SocketIO()
migrate = Migrate()
jwt = JWTManager()

DB_NAME = 'app.db'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Load configuration
    if config_name == 'testing':
        app.config.from_object(TestingConfig)  # Use TestingConfig for testing
    else:
        app.config.from_object(Config)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=31)  # Token expiry

    # Initialize extensions
    db.init_app(app)
    skt.init_app(app, cors_allowed_origins=["http://localhost:8000"])
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Enable CORS
    CORS(app, origins=["http://localhost:8000", "http://localhost:3000"])  # Add other origins as needed

    
    # Register blueprints
    from .auth.routes import authbp
    from .groups.routes import groupsbp

    app.register_blueprint(authbp)
    app.register_blueprint(groupsbp)

    # Create database if it doesn't exist
    if config_name != 'testing':
        create_database(app)
    
    return app

@skt.on('some_event')
def handle_some_event(data):
    print('Received data:', data)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_database(app):
    if not path.exists('app/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Database created!')
