from flask import Flask
from flask_socketio import SocketIO, emit, join_room
import json
from .models import chat_model

ChatWSapp = Flask(__name__)
socketio = SocketIO(ChatWSapp)

@ChatWSapp.route('/')
def index():
    return 

clients_cache = []

@socketio.on('open')
def on_connection_established():
    emit('connect',{'message':'conected'})
    
@socketio.on('register')
def on_connection_established(reg):
    clients_cache.append({"client_id":reg})   
    join_room(reg)
    emit('connect',{'message':'conected'})

@socketio.on('reconnect')
def on_connection_established(reg):
    clients_cache.append({"client_id":reg})   
    join_room(reg)
    emit('connect',{'message':'conected'})
    
@socketio.on('message')
def message_parse(message):
    '''
    data from front-end :: data in back-end
     message :: message
     send_date_and_time :: date_created
     sent_to :: recipent
     sent_from :: sender
    '''
    decoded_message = json.loads(message)
    if decoded_message is not None:
        emit('message',decoded_message,room=decoded_message['sent_to'])
        #TODO: store sent message to the database
        chat = chat_model.Chat(decoded_message['message'],decoded_message['send_date_and_time']
                                ,decoded_message['sent_to'],decoded_message['sent_from'])
        chat.save_to_db()

@socketio.on("error")
def handle_error():
    pass

@socketio.on("close")
def close_connection(user_id):
    socketio.close_room(user_id)
    emit('close',{'message':'closed chat'})

if __name__ == '__main__':
    socketio.run(ChatWSapp,port=3000)