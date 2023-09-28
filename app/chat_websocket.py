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
    '''
    data from front-end :: data in back-end
     message :: message
     send_date_and_time :: date_created
     sent_to :: recipient
     sent_from :: sender
    '''
    decoded_message = json.loads(data)
    if decoded_message is not None:
        message_type = decoded_message.get('type')
        if message_type == 'register':
            join_room(decoded_message['register_id'])
        elif message_type == 'message':
            emit('message', decoded_message, room=decoded_message['sent_to'])
            # TODO: Store sent message to the database
            chat = chat_model.Chat(
                decoded_message['message'],
                decoded_message['send_date_and_time'],
                decoded_message['sent_to'],
                decoded_message['sent_from']
            )
            chat.save_to_db()


@socketio.on("error")
def handle_error(data):
    pass


@socketio.on('typing')
def handle_typing(data):
    emit('typing', data, room=data['recipient'])


@socketio.on('read')
def handle_read(data):
    emit('read', data, room=data['recipient'])

# You can add more events as needed based on our chat feature requirements
