from db import db
from .user_model import User


class Buyer(User):
    __tablename__ = "buyers"

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    # Add Buyer-specific attributes here

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Add Buyer-specific methods here
