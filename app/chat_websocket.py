from flask import session
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from app.models import User, Chat, Message, ChatMessage

socketio = SocketIO()


# clients_cache = []

@socketio.on('message')
def handle_con_message(data):
    print(data)

    send({"msg": data['data'], "conf_id": "1"})


@socketio.on('getChat')
def get_chat(data):
    rid = data['rid']
    user_id = data["userId"]
    user_chats = Chat.query.filter_by(user_id=user_id).first()
    chat_list = user_chats.chat_list if user_chats else []

    # Getting the chat info from the room id
    chat = {}
    for c in chat_list:
        if c["room_id"] == rid:
            user = User.query.filter_by(c["user_id"])
            name = user.username
            image = user.image
            chat["name"] = name
            chat["user_img"] = image
            chat["room_id"] = c["room_id"]

    emit('getChatJS', {"chat": chat, })


@socketio.on('getChats')
def send_chats(data):
    user_id = data['userId']
    user_chats = Chat.query.filter_by(user_id=user_id).first()
    chat_list = user_chats.chat_list if user_chats else []

    ch = []
    chat_count = len(chat_list)
    i = 0
    for c in chat_list:

        # Query the database to get the username and image of users in a user's chat
        user = User.query.filter_by(c["user_id"])
        username = user.username
        image = user.image

        try:
            # Get the Message object for the chat room
            message = Message.query.filter_by(room_id=c["room_id"]).first()

            # Get the last ChatMessage object in the Message's messages relationship
            last_message = message.messages[-1]

            # Get the message content of the last ChatMessage object
            last_message_content = last_message.content
        except (AttributeError, IndexError):
            # Set variable to this when no messages have been sent to the room
            last_message_content = "This place is empty. No messages ..."

        ch.append({i: {
            'id': c["room_id"],
            'name': username,
            'user_img': image,
            'last_message': last_message_content
        }})
        i = i + 1
    emit('getChatsJS', {"chats": ch, "chatCount": chat_count, "user": User.query.filter_by(user_id).username})


@socketio.on('getMessages')
def send_messages(data):
    chats = Message.query.filter_by(room_id=data['rid']).first().messages if data else []
    chats_count = len(chats)
    i = 0
    ch = []
    room = data['rid']
    join_room(room)
    for c in chats:
        ch.append({i: {
            'id': c.id,
            'message': c.content,
            'sender_id': c.sender_id,
            'rid': c.room_id,
            'image': c.image
        }})
        i = i + 1
    emit('receiveMessageJS', {"chats": ch, "room_id": room}, broadcast=True)


# Join-chat event. Emit online message to other users and join the room
@socketio.on('join-chat')
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
@socketio.on('sendMessage')
def handle_message(data, methods=["GET", "POST"]):
    room_id = data["rid"]
    timestamp = data["timestamp"]
    content = data["message"]
    sender_id = data["sender_id"]

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

    data["image"] = 0

    # Emit the message(s) sent to other users in the room
    socketio.emit(
        "receiveMessage",
        data,
        # room=room_id,
        # include_self=False,
    )


@socketio.on('sendImage')
def send_image(data, methods=["GET", "POST"]):
    # Get ChatMessage id with session['image_id'] (logic handled in upload image route)
    if ChatMessage.query.filter_by(id=session['imageid']).count() == 1:
        chat_message = ChatMessage.query.filter_by(id=session['imageid']).first()
        session['image_id'] = -1  # image sent

        data = {
            'message': chat_message.content,
            # 'sender_username': User.query.filter_by(id=data["sender_id"]).username,
            'sender_id': data["sender_id"],
            'rid': chat_message.room_id,
            'timestamp': chat_message.timestamp,
            'image': 1
        }

        # Emit the message(s) sent to other users in the room
        socketio.emit(
            "receiveMessage",
            data,
            # room=data["room_id"],
            # include_self=False,
        )


@socketio.on('typing')
def handle_typing(data):
    emit('typing', data, room=data['recipient'])


@socketio.on('read')
def handle_read(data):
    emit('read', data, room=data['recipient'])


@socketio.on('error')
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
