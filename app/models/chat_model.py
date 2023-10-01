from db import db
from datetime import date
from .group_chats import group_chats

import hashlib
import uuid


class Chat(db.Model):
    __tablename__ = "chats"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(400), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    sender = db.Column(db.String(400), db.ForeignKey("users.id"), nullable=False)
    recipient = db.Column(db.String(400), db.ForeignKey("users.id"), nullable=False)

    # Define the relationship with the User model
    sender_user = db.relationship("User", foreign_keys=[sender], back_populates="sent_chats")
    recipient_user = db.relationship("User", foreign_keys=[recipient], back_populates="received_chats")

    def __init__(self, message, timestamp, recipient, sender):
        self.message = message
        self.timestamp = timestamp
        self.recipient = recipient
        self.sender = sender

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

    def retrieve_all_chats_between_users(self, user_id, date_start, date_end):
        """
        Retrieves all chats between the current user and another user within a specified date range.

        Args:
            user_id (str): The unique_id of the current user.
            date_start (date): The start date for filtering chats.
            date_end (date): The end date for filtering chats.

        Returns:
            list: List of dictionaries representing chat bundles.
        """
        return group_chats(
            Chat.query.filter(
                (Chat.sender == user_id) | (Chat.recipient == user_id),
                (date_start <= Chat.timestamp <= date_end)
            ).order_by(Chat.timestamp.asc()).all()
        )

    def retrieve_chats_between_users(self, user1_id, user2_id, date_start, date_end):
        """
        Retrieves chats between two users within a specified date range.

        Args:
            user1_id (str): The unique_id of the first user.
            user2_id (str): The unique_id of the second user.
            date_start (date): The start date for filtering chats.
            date_end (date): The end date for filtering chats.

        Returns:
            list: List of dictionaries representing chat bundles.
        """
        return Chat.query.filter(
            ((Chat.sender == user1_id) & (Chat.recipient == user2_id)) |
            ((Chat.sender == user2_id) & (Chat.recipient == user1_id)),
            (date_start <= Chat.timestamp <= date_end)
        ).order_by(Chat.timestamp.asc()).all()
