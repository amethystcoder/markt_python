from db import db
import hashlib
import uuid


class Favorite(db.Model):
    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    buyer_id = db.Column(db.String(400), db.ForeignKey('buyers.unique_id'), nullable=False)
    favorite_item_id = db.Column(db.String(400), nullable=False) #the id of the buyer favorite (seller or product)
    favorite_type = db.Column(db.String(400), nullable=False) #seller or product

    # Define relationships
    buyer = db.relationship("Buyer", back_populates="favorites")

    """
    def __init__(self,buyer_id,product_id,id):
        if id is not None:
            self = self.get_favorite_using_id(id)
        else:
            self.buyer_id = buyer_id
            self.product_id = product_id
            
    """
    
    @classmethod
    def get_favorite_using_id(cls, _id):
        return cls.query.filter_by(id == _id).first()
    
    @classmethod
    def delete_all_buyer_favorites(cls, buyer_id):
        return cls.filter_by(buyer_id == buyer_id).delete()

    @classmethod
    def get_all_buyer_favorites(cls, buyer_id):
        return cls.query.filter_by(buyer_id == buyer_id).all()
    
    @classmethod
    def get_all_buyer_favorites_that_are_sellers(cls, buyer_id):
        return cls.query.filter_by(buyer_id == buyer_id).filter(Favorite.favorite_type == "seller").all()
    
    @classmethod
    def get_all_buyer_favorites_that_are_products(cls, buyer_id):
        return cls.query.filter(buyer_id == buyer_id).filter(Favorite.favorite_type == "product").all()

    @staticmethod
    def generate_unique_id():
        unique_id = str(uuid.uuid4()).encode()
        return hashlib.sha256(unique_id).hexdigest()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
