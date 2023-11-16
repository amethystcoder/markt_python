from db import db
from .user_model import User


class Buyer(User):
    __tablename__ = "buyers"

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    unique_id = db.Column(db.String(400), nullable=False, unique=True)
    # Add Buyer-specific attributes here
    
    username = db.Column(db.String(80), unique=True, nullable=False)
    
    def __init__(self,unique_id,username):
        if unique_id is not None:
            self = self.get_buyer(unique_id=unique_id)
        else:
            self.username = username
            
    def get_buyer(self,unqiue_id):
        return db.session.query(Buyer).filter(Buyer.unique_id == unqiue_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    # Add Buyer-specific methods here
