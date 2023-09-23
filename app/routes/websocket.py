from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from json import decoder,encoder

ChatWSapp = Flask(__name__)
socketio = SocketIO(ChatWS)

@ChatWSapp.route('/')
def index():
    return 

clients_cache = {}

@socketio.on('connect')
def test_connect():
    socketio.emit('after connect', {'data', 'hello'})
    
@socketio.on('message')
def message_parse(message):
    decoded_message = decoder.JSONDecoder.decode(message)
    match decoded_message['type']:
        case '':
            pass
        case '':
            pass
        case _:
            pass


if __name__ == '__main__':
    socketio.run(ChatWSapp)