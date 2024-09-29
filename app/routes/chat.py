from flask import request
from flask_socketio import emit, join_room, leave_room
from flask_login import current_user, login_required
from .. import socketio
from ..models.user_model import User
from ..models.product_model import Product
from ..models.chat_model import ChatMessage, ChatRoom


@socketio.on('connect')
@login_required
def handle_connect():
    emit('connected', {'data': f'Connected as {current_user.id}'})


@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('status', {'msg': f'{current_user.id} has entered the room.'}, room=room)


@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)
    emit('status', {'msg': f'{current_user.id} has left the room.'}, room=room)


@socketio.on('message')
def handle_message(data):
    room = data['room']
    message = data['message']
    user_id = current_user.id

    # Save message to database
    chat_message = ChatMessage(sender_id=user_id, room_id=room, content=message)
    chat_message.save_to_db()

    emit('message', {'user': user_id, 'msg': message}, room=room)


@socketio.on('product_share')
def handle_product_share(data):
    room = data['room']
    product_id = data['product_id']
    user_id = current_user.id

    # Fetch product details and emit to room
    product = Product.query.get(product_id)
    if product:
        emit('product_shared', {
            'user': user_id,
            'product': {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                # Add other relevant product details
            }
        }, room=room)
