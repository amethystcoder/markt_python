from flask_socketio import SocketIO, emit, join_room, leave_room
import json
from .models import Chat

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
        message_type = decoded_message.get('type')

        if message_type in ['text', 'image', 'product']:
            # Handle different message types
            # For simplicity, I'll assume 'text' and 'image' for now
            message_content = decoded_message.get('content', '')

            chat = Chat(
                message_type=message_type,
                message_content=message_content,
                sender=decoded_message['sender'],
                recipient=decoded_message['recipient']
            )
            chat.save_to_db()

            emit('message', decoded_message, room=decoded_message['recipient'])


@socketio.on('typing')
def handle_typing(data):
    emit('typing', data, room=data['recipient'])


@socketio.on('read')
def handle_read(data):
    emit('read', data, room=data['recipient'])

# You can add more events as needed based on your chat feature requirements
