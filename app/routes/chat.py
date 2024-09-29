from flask import request, jsonify
from flask_smorest import Blueprint
from flask_socketio import emit, join_room, leave_room
from flask_login import current_user, login_required
from .. import socketio, db
from ..models.user_model import User
from ..models.chat_model import ChatMessage, ChatRoom
from ..models.product_model import Product
from ..schemas import ChatMessageSchema, ChatRoomSchema
from sqlalchemy.exc import SQLAlchemyError

chat_bp = Blueprint("chat", __name__, description="Chat operations")


@socketio.on('connect')
@login_required
def handle_connect():
    emit('connected', {'data': f'Connected as {current_user.id}'})


@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('status', {'msg': f'User {current_user.id} has entered the room.'}, room=room)


@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)
    emit('status', {'msg': f'User {current_user.id} has left the room.'}, room=room)


@socketio.on('message')
def handle_message(data):
    room = data['room']
    message = data['message']

    try:
        chat_message = ChatMessage(sender_id=current_user.id, room_id=room, content=message)
        db.session.add(chat_message)
        db.session.commit()

        emit('message', {'user': current_user.id, 'msg': message}, room=room)
    except SQLAlchemyError as e:
        db.session.rollback()
        emit('error', {'msg': 'Failed to save message'}, room=room)


@socketio.on('product_share')
def handle_product_share(data):
    room = data['room']
    product_id = data['product_id']

    product = Product.query.get(product_id)
    if product:
        try:
            chat_message = ChatMessage(
                sender_id=current_user.id,
                room_id=room,
                content=f"Shared product: {product.name}",
                is_product_share=True,
                product_id=product_id
            )
            db.session.add(chat_message)
            db.session.commit()

            emit('product_shared', {
                'user': current_user.id,
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'description': product.description,
                    'image_url': product.image_url  # Assuming you have an image_url field
                }
            }, room=room)
        except SQLAlchemyError as e:
            db.session.rollback()
            emit('error', {'msg': 'Failed to share product'}, room=room)
    else:
        emit('error', {'msg': 'Product not found'}, room=room)


@chat_bp.route('/rooms', methods=['POST'])
@login_required
def create_chat_room():
    data = request.json
    buyer_id = data.get('buyer_id')
    seller_id = data.get('seller_id')

    if current_user.id != buyer_id and current_user.id != seller_id:
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        chat_room = ChatRoom(buyer_id=buyer_id, seller_id=seller_id)
        db.session.add(chat_room)
        db.session.commit()
        return ChatRoomSchema().dump(chat_room), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create chat room'}), 500


@chat_bp.route('/rooms/<int:room_id>/messages', methods=['GET'])
@login_required
def get_chat_messages(room_id):
    chat_room = ChatRoom.query.get(room_id)

    if not chat_room or (current_user.id != chat_room.buyer_id and current_user.id != chat_room.seller_id):
        return jsonify({'error': 'Unauthorized'}), 403

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    messages = ChatMessage.query.filter_by(room_id=room_id).order_by(ChatMessage.timestamp.desc()).paginate(page=page,
                                                                                                            per_page=per_page)

    return jsonify({
        'messages': ChatMessageSchema(many=True).dump(messages.items),
        'total': messages.total,
        'pages': messages.pages,
        'current_page': messages.page
    })
