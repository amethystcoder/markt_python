from db import db
from datetime import date

import hashlib
import uuid


class Chat(db.Model):
    __tablename__ = "chats"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    chat_list = db.Column(db.JSON, nullable=False, default=list)

    # Define the relationship with the User model
    user = db.relationship('User', backref=db.backref('chats', lazy=True))

    @staticmethod
    def generate_unique_id():
        """
        Generate a unique ID for a chat message using SHA256 and a UUID.
        """
        unique_id = str(uuid.uuid4())
        hashed_id = hashlib.sha256(unique_id.encode()).hexdigest()
        return hashed_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.String(50), nullable=False, unique=True)
    messages = db.relationship('ChatMessage', backref='message', lazy=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_type = db.Column(db.String(50), nullable=False, default='text')  # 'text', 'image', etc
    content = db.Column(db.String(400))
    image_url = db.Column(db.String(255))  # handling image messages
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    sender_id = db.Column(db.Integer, nullable=False)
    room_id = db.Column(db.String(50), db.ForeignKey('messages.room_id', nullable=False))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
