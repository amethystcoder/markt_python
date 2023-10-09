from flask_socketio import SocketIO, emit, join_room, leave_room
import json


from app import Chat
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
        if message_type == 'register':
            join_room(decoded_message['register_id'])
        elif message_type == 'message':
            unique_id = Chat.generate_unique_id()
            emit('message', decoded_message, room=decoded_message['sent_to'])

            message_content = decoded_message.get('message', '')
            image_url = decoded_message.get('image_url', None)
            product_name = decoded_message.get('product_name', None)

            chat = Chat(
                unique_id=unique_id,
                message=message_content,
                timestamp=decoded_message['send_date_and_time'],
                recipient=decoded_message['sent_to'],
                sender=decoded_message['sent_from'],
                message_type=decoded_message.get('message_type', 'text'),  # default to 'text'
                image_url=image_url,
                product_name=product_name
            )
            chat.save_to_db()


@socketio.on('typing')
def handle_typing(data):
    emit('typing', data, room=data['recipient'])


@socketio.on('read')
def handle_read(data):
    emit('read', data, room=data['recipient'])

# You can add more events as needed based on your chat feature requirements


"""if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)"""
