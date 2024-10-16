from flask import Flask
from flask_socketio import SocketIO

skt = SocketIO()

def create_app():
   app= Flask(__name__)
   app.config['SECRET_KEY'] ='asdfghj'
   skt.init_app(app)
   return app

