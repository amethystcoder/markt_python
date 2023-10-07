from db import db
from datetime import date

import hashlib
import uuid


class Chat(db.Model):
    __tablename__ = "chats"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message_type = db.Column(db.String(20), nullable=False)  # 'text', 'image', 'product'
    message_content = db.Column(db.String(400))  # For text and image, for product, consider a relationship
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    sender = db.Column(db.String(400), db.ForeignKey("users.id"), nullable=False)
    recipient = db.Column(db.String(400), db.ForeignKey("users.id"), nullable=False)

    # Define the relationship with the User model
    sender_user = db.relationship("User", foreign_keys=[sender], back_populates="sent_chats")
    recipient_user = db.relationship("User", foreign_keys=[recipient], back_populates="received_chats")

    def __init__(self, message_type, message_content, sender, recipient):
        self.message_type = message_type
        self.message_content = message_content
        self.sender = sender
        self.recipient = recipient

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

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
