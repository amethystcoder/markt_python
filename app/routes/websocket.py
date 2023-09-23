from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
import json

ChatWSapp = Flask(__name__)
socketio = SocketIO(ChatWSapp)

@ChatWSapp.route('/')
def index():
    return 

#clients = test_client.SocketIOTestClient.clients
clients_cache = {}

@socketio.on('connect')
def on_connection_established():
    socketio.emit('connect',{'message':'conected'})
    
@socketio.on('message')
def message_parse(message):
    decoded_message = json.loads(message)
    if decoded_message is not None:
        if decoded_message['type'] is not None:
            match decoded_message['type']:
                case 'register':
                    decoded_message['register_id']
                    pass
                case 'message':
                    pass
                case _:
                    pass
        else:
            pass


if __name__ == '__main__':
    socketio.run(ChatWSapp,port=3000)