"""This module, 'websocket.py', is typically responsible for handling WebSocket connections related to various
functionalities of your ecommerce platform, which may not be directly related to chat.
It could be used for real-time updates of product availability, notifications, or other interactive features.

Example Code (websocket.py):

"""

from flask_socketio import SocketIO, emit

socketio = SocketIO()


@socketio.on('connect')
def handle_connect():
    # This event is triggered when a client connects to the WebSocket server.
    print('Client connected.')


@socketio.on('disconnect')
def handle_disconnect():
    # This event is triggered when a client disconnects from the WebSocket server.
    print('Client disconnected.')


@socketio.on('product_update')
def handle_product_update(data):
    # Example: Notify clients about a product update.
    product_id = data['product_id']
    emit('product_updated', {'product_id': product_id}, broadcast=True)
