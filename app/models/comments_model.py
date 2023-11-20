from db import db
import time
import hashlib
import uuid


class Comments(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment_id = db.Column(db.String(400), nullable=False)
    comment_title = db.Column(db.String(400), nullable=False)
    buyer_id = db.Column(db.String(400), db.ForeignKey('buyers.unique_id'), nullable=False)
    buyer_name = db.Column(db.String(400), nullable=False)
    comment_place_id = db.Column(db.String(400), nullable=False) #the id of the place the comment is created
    comment_date = db.Column(db.TIMESTAMP, nullable=False)

    # Define relationships
    buyer = db.relationship("Buyer", back_populates="comments")
    product = db.relationship("Product", back_populates="comments")
    seller = db.relationship("Seller",back_populates="comments")
    
    def __init__(self,comment_title,buyer_id,buyer_name,comment_place_id,comment_id):
        if comment_id is not None:
            self = self.get_comment_using_id(comment_id)
        else:
            self.comment_title = comment_title
            self.buyer_id = buyer_id
            self.buyer_name = buyer_name
            self.comment_place_id = comment_place_id
            self.comment_date = time.time()
    
    def generate_unique_id():
        unique_id = str(uuid.uuid4()).encode()
        return hashlib.sha256(unique_id).hexdigest()
    
    @classmethod
    def get_comment_using_id(self,comment_id):
        return db.session.query(Comments).filter(Comments.comment_id == comment_id).first()
    
    @classmethod
    def get_product_comments(self,product_id):
        return db.session.query(Comments).filter(Comments.comment_place_id == product_id).all()
    
    @classmethod
    def get_buyer_comments(self,buyer_id):
        return db.session.query(Comments).filter(Comments.buyer_id == buyer_id).all()
    
    @classmethod
    def get_seller_comments(self,seller_id):
        return db.session.query(Comments).filter(Comments.comment_place_id == seller_id).all()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
