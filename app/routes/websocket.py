from flask import Flask
from flask_socketio import SocketIO, emit, join_room

ChatWSapp = Flask(__name__)
socketio = SocketIO(ChatWSapp)

@ChatWSapp.route('/')
def index():
    return 

@socketio.on("error")
def handle_error():
    pass
