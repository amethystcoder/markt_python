from db import db
from .user_model import User


class Buyer(User):
    __tablename__ = "buyers"

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    unique_id = db.Column(db.String(400), nullable=False, unique=True)
    # Add Buyer-specific attributes here
    
    username = db.Column(db.String(80), unique=True, nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Add Buyer-specific methods here
