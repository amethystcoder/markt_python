from flask_socketio import SocketIO, emit, join_room, leave_room
from app.models import User, Chat, Message, ChatMessage

socketio = SocketIO()


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
@socketio.on("outgoing")
def handle_text_message(json, methods=["GET", "POST"]):
    room_id = json["rid"]
    timestamp = json["timestamp"]
    content = json["content"]
    #message_type = json["message_type"]
    sender_id = json["sender_id"]

    # Get the message entry for the chat room
    message_entry = Message.query.filter_by(room_id=room_id).first()

    # Add the new message to the conversation
    chat_message = ChatMessage(
        content=content,
        #message_type=message_type,
        timestamp=timestamp,
        sender_id=sender_id,
        room_id=room_id,
    )
    # Add the new chat message to the messages relationship of the message
    message_entry.messages.append(chat_message)

    # Updated the database with the new message
    chat_message.save_to_db()
    message_entry.save_to_db()

    # Emit the message(s) sent to other users in the room
    socketio.emit(
        "message",
        json,
        room=room_id,
        include_self=False,
    )


@socketio.on("imageData")
def handle_image_message(json, methods=["GET", "POST"]):
    room_id = json["rid"]
    timestamp = json["timestamp"]
    image_url = json["image_url"]
    #message_type = json["message_type"]
    sender_id = json["sender_id"]

    # Get the message entry for the chat room
    message_entry = Message.query.filter_by(room_id=room_id).first()

    # Add the new message to the conversation
    chat_message = ChatMessage(
        image_url=image_url,
        message_type="image",
        timestamp=timestamp,
        sender_id=sender_id,
        room_id=room_id,
    )
    # Add the new chat message to the messages relationship of the message
    message_entry.messages.append(chat_message)

    # Updated the database with the new message
    chat_message.save_to_db()
    message_entry.save_to_db()

    # Emit the message(s) sent to other users in the room
    socketio.emit(
        "message",
        json,
        room=room_id,
        include_self=False,
    )


@socketio.on('typing')
def handle_typing(data):
    emit('typing', data, room=data['recipient'])


@socketio.on('read')
def handle_read(data):
    emit('read', data, room=data['recipient'])


# You can add more events as needed based on your chat feature requirements


"""if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)"""
