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
    
    def __init__(self,unique_id,shop_name,description,category,total_rating,total_raters,directions):
        if unique_id is not None:
            self = self.get_seller(uniue_id=unique_id)
        else:
            self.shop_name = shop_name
            self.description = description
            self.category = category
            self.total_rating = total_rating
            self.total_raters = total_raters
            self.directions = directions
            
    def get_seller(self,uniue_id):
        return db.session.query(Seller).filter(Seller.unique_id == uniue_id).first()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # Add Seller-specific methods here
