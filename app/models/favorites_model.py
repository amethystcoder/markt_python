from db import db
import hashlib
import uuid


class Favorite(db.Model):
    __tablename__ = "favortites"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    buyer_id = db.Column(db.String(400), db.ForeignKey('buyers.unique_id'), nullable=False)
    favorite_item_id = db.Column(db.String(400), nullable=False) #the id of the buyer favorite (seller or product)
    favorite_type = db.Column(db.String(400), nullable=False) #seller or product

    # Define relationships
    buyer = db.relationship("Buyer", back_populates="favorites")
    
    def __init__(self,buyer_id,product_id,id):
        if id is not None:
            self = self.get_favorite_using_id(id)
        else:
            self.buyer_id = buyer_id
            self.product_id = product_id
    
    def generate_unique_id():
        unique_id = str(uuid.uuid4()).encode()
        return hashlib.sha256(unique_id).hexdigest()
    
    @classmethod
    def get_favorite_using_id(self,id):
        return db.session.query(Favorite).filter(Favorite.id == id).first()
    
    @classmethod
    def delete_all_buyer_favorites(self,buyer_id):
        return db.session.query(Favorite).filter(Favorite.buyer_id == buyer_id).delete()
    
    @classmethod
    def get_all_buyer_favorites_that_are_sellers(self,buyer_id):
        return db.session.query(Favorite).filter(Favorite.buyer_id == buyer_id).filter(Favorite.favorite_type == "seller").all()
    
    @classmethod
    def get_all_buyer_favorites_that_are_products(self,buyer_id):
        return db.session.query(Favorite).filter(Favorite.buyer_id == buyer_id).filter(Favorite.favorite_type == "product").all()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
