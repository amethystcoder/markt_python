from db import db

class Chat(db.Model):
    """
    Controls all database crud operations related to user chats 
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

    def __init__(self,user_id):
        pass

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def arrange_chats(self, chats, user_id):
        '''
        arranges all unarranged chats of a particular user into packs of 
        
        '''
        pass

    def retrieve_all_chats_using_user_id(self,user_id):
        """
        Gets all messages connected to a user(buyer or seller).
        gets all messages, chats e.t.c from the database where the 
        sender or recipent of the chat is the user with the `user_id`

        Args:
            user_id (String): _description_
            The specified unique_id of the user(buyer/seller)
        """
        return db.session.query(Chat).get({'sender':user_id})
    
    def retrieve_chats_in_date_packets_using_user_id(self,user_id):
        return db.session.query(Chat).get({'sent_from':user_id})

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
