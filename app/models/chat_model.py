from db import db
from datetime import date
from .arrange_chats import arrange_chats

class Chat(db.Model):
    """Controls all database crud operations related to user chats 
    """
    
    __tablename__ = "chats"

    #An incremental id for the specified chat
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #a unique identifier for a specific chat SHA256 Encoded
    unique_id = db.Column(db.String(400), nullable=False, unique=True)
    #The message sent  
    message = db.Column(db.String(400), nullable=False)
    date_created = db.Column(db.TIMESTAMP, nullable=False)
    recipent = db.Column(db.String(400), nullable=False)
    #The user who sent the chat
    sender = db.Column(db.String(400), nullable=False)

    def __init__(self,unique_id,message,date_created,recipent,sender):
        self.unique_id = unique_id
        self.message = message
        self.date_created = date_created
        self.recipent = recipent
        self.sender = sender

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def retrieve_all_chats_using_user_id(self,user_id):
        """Gets all messages connected to a user(buyer or seller).
        gets all messages, chats e.t.c from the database where the 
        sender or recipent of the chat is the user with the `user_id`

        Args:
            user_id (String):
            The specified unique_id of the user(buyer/seller)
        """
        return arrange_chats(
            db.session.query(Chat).filter(Chat.sender == user_id or Chat.recipent == user_id).all()
            )
    
    def retrieve_chats_in_date_packets_using_user_id(self,sender_id,recipent_id,date):
        ''' 
        This function retrieves chats between two users from a particular date to another
        sender_id is the id of one of the users
        recipent_id is the id of the other user
        
        '''
        return db.session.query(Chat).filter(
            Chat.sender == sender_id or Chat.recipent == sender_id
            or Chat.sender == recipent_id or Chat.recipent == recipent_id
            ).filter(Chat.date_created == '').all()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

