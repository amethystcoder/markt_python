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

    def __init__(self, unique_id, message, date_created, recipient, sender):
        self.unique_id = unique_id
        self.message = message
        self.date_created = date_created
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

    def retrieve_all_chats_using_user_id(self, user_id, date_start, date_end):
        """Gets all messages connected to a user(buyer or seller).
        gets all messages, chats e.t.c from the database where the 
        sender or recipent of the chat is the user with the `user_id` 
        from a particular date to another

        Args:
            user_id (String):
            The specified unique_id of the user(buyer/seller)
            :param user_id:
            :param date_end:
            :param date_start:
        """
        return group_chats(
            db.session.query(Chat).filter(Chat.sender == user_id or Chat.recipent == user_id)
            .filter(
                date(date_start['year'], date_start['month'], date_start['day']) <= Chat.date_created <= date(
                    date_end['year'], date_end['month'], date_end['day'])
            ).order_by(Chat.date_created.asc()).all()
        )

    def retrieve_chats_in_date_packets_using_user_id(self, sender_id, recipent_id, date_start, date_end):
        ''' 
        
        This function retrieves chats between two users from a particular date to another
        sender_id is the id of one of the users
        recipent_id is the id of the other user
        
        '''
        return db.session.query(Chat).filter(
            Chat.sender == sender_id or Chat.recipent == sender_id
            or Chat.sender == recipent_id or Chat.recipent == recipent_id
        ).filter(
            date(date_start['year'], date_start['month'], date_start['day']) <= Chat.date_created <= date(
                date_end['year'], date_end['month'], date_end['day'])
        ).order_by(Chat.date_created.asc()).all()
