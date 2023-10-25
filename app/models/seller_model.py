from db import db
from .user_model import User


class Seller(User):
    __tablename__ = "sellers"

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    unique_id = db.Column(db.String(400), nullable=False, unique=True)
    # Add Seller-specific attributes here
    shop_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    total_rating = db.Column(db.Integer, nullable=False)
    total_raters = db.Column(db.Integer, nullable=False)
    directions = db.Column(db.String(400), nullable=False)

    # Define a one-to-many relationship between Seller and Product
    products = db.relationship('Product', back_populates='seller')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # Add Seller-specific methods here
