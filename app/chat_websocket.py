from flask import session
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from app.models import User, Chat, Message, ChatMessage

socketio = SocketIO()


# clients_cache = []

@socketio.on('message')
def handle_con_message(data):
    print(data)

    send({"msg": data['data'], "conf_id": "1"})


# Join-chat event. Emit online message to other users and join the room
@socketio.on("join-chat")
def join_private_chat(data):
    room = data["rid"]
    join_room(room=room)
    socketio.emit(
        "joined-chat",
        {"msg": f"{room} is now online."},
        room=room,
        # include_self=False,
    )


# Outgoing event handler
@socketio.on("sendMessage")
def handle_message(json, methods=["GET", "POST"]):
    room_id = json["rid"]
    timestamp = json["timestamp"]
    content = json["message"]
    sender_id = json["sender_id"]

    # Get the message entry for the chat room
    message_entry = Message.query.filter_by(room_id=room_id).first()

    # Add the new message to the conversation
    chat_message = ChatMessage(
        content=content,
        image=0,
        timestamp=timestamp,
        sender_id=sender_id,
        room_id=room_id,
    )
    # Add the new chat message to the messages relationship of the message
    message_entry.messages.append(chat_message)

    # Updated the database with the new message
    chat_message.save_to_db()
    message_entry.save_to_db()

    json["image"] = 0

    # Emit the message(s) sent to other users in the room
    socketio.emit(
        "receiveMessage",
        json,
        room=room_id,
        include_self=False,
    )


@socketio.on("sendImage")
def send_image(json, methods=["GET", "POST"]):
    # Get ChatMessage id with session['image_id'] (logic handled in upload image route)
    if ChatMessage.query.filter_by(id=session['imageid']).count() == 1:
        chat_message = ChatMessage.query.filter_by(id=session['imageid']).first()
        session['image_id'] = -1  # image sent

        json = {
            'message': chat_message.content,
            'sender_username': User.query.filter_by(id=json["sender_id"]).username,
            'rid': chat_message.room_id,
            'timestamp': chat_message.timestamp,
            'image': 1
        }

        # Emit the message(s) sent to other users in the room
        socketio.emit(
            "receiveMessage",
            json,
            room=json["room_id"],
            include_self=False,
        )


@socketio.on('typing')
def handle_typing(data):
    emit('typing', data, room=data['recipient'])


@socketio.on('read')
def handle_read(data):
    emit('read', data, room=data['recipient'])


@socketio.on("error")
def handle_error():
    pass


"""@socketio.on('disconnect')
def handle_disconnect(data):
    user_id = data['user_id']
    leave_room(user_id)
    emit('disconnect', {'message': 'disconnected'})


@socketio.on('register')
def on_connection_established(reg):
    clients_cache.append({"client_id": reg})
    join_room(reg)
    emit('connect', {'message': 'conected'})


@socketio.on('reconnect')
def on_connection_established(reg):
    clients_cache.append({"client_id": reg})
    join_room(reg)
    emit('connect', {'message': 'conected'})
    
    @socketio.on("close")
    def close_connection(user_id):
        socketio.close_room(user_id)
        emit('close',{'message':'closed chat'})"""

# You can add more events as needed based on your chat feature requirements


"""if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)"""
