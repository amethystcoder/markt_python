from db import db


class Chat(db.Model):
    __tablename__ = "chats"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(400), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    recipient = db.Column(db.String(400), nullable=False)
    sender = db.Column(db.String(400), nullable=False)

    def __init__(self, message, recipient, sender):
        self.message = message
        self.recipient = recipient
        self.sender = sender

    def save_to_db(self, session):
        session.add(self)

    def delete_from_db(self, session):
        session.delete(self)
