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
    sent_to = db.Column(db.String(400), nullable=False)
    sent_from = db.Column(db.String(400), nullable=False)

    def __init__(self,user_id):
        pass

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def retrieve_chats_using_id(self,id):
        db.session.select()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
