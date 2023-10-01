from flask_socketio import SocketIO, emit, join_room, leave_room
import json
from .models import chat_model

socketio = SocketIO()


@socketio.on('connect')
def handle_connect(data):
    user_id = data['user_id']
    join_room(user_id)
    emit('connect', {'message': 'connected'})


@socketio.on('disconnect')
def handle_disconnect(data):
    user_id = data['user_id']
    leave_room(user_id)
    emit('disconnect', {'message': 'disconnected'})


@socketio.on('message')
def handle_message(data):
    decoded_message = json.loads(data)
    if decoded_message is not None:
        # Handle message processing and broadcasting here
        # You can save the message to the database, emit it to recipients, etc.
        emit('message', decoded_message, room=decoded_message['sent_to'])


@socketio.on('typing')
def handle_typing(data):
    emit('typing', data, room=data['recipient'])


@socketio.on('read')
def handle_read(data):
    emit('read', data, room=data['recipient'])

# You can add more events as needed based on your chat feature requirements
