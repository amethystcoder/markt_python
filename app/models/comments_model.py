from db import db
import time
import hashlib
import uuid


class Comments(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.String(400), nullable=False)
    comment_title = db.Column(db.String(400), nullable=False)
    # buyer_id = db.Column(db.String(400), db.ForeignKey('buyers.unique_id'), nullable=False)
    buyer_name = db.Column(db.String(400), nullable=False)
    comment_place_id = db.Column(db.String(400), nullable=False)  # the id of the place the comment is created
    comment_date = db.Column(db.TIMESTAMP, nullable=False)

    # Define relationships
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyers.id'), nullable=False)
    buyer = db.relationship("Buyer", back_populates="comments")

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship("Product", back_populates="comments")

    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'), nullable=False)
    seller = db.relationship("Seller", back_populates="comments")

    @staticmethod
    def generate_unique_id():
        unique_id = str(uuid.uuid4()).encode()
        return hashlib.sha256(unique_id).hexdigest()

    def parse_comment(self):
        return {
            "id": self.id,
            "comment_id": self.comment_id,
            "comment_title": self.comment_title,
            "buyer_id": self.buyer_id,
            "buyer_name": self.buyer_name,
            "comment_place_id": self.comment_place_id,
            "comment_date": self.comment_date
        }

    @classmethod
    def get_comment_using_id(cls, comment_id):
        return cls.query.filter_by(comment_id=comment_id).first()

    @classmethod
    def get_product_comments(cls, product_id):
        return cls.query.filter_by(comment_place_id=product_id).all()

    @classmethod
    def get_buyer_comments(cls, buyer_id):
        return cls.query.filter_by(buyer_id=buyer_id).all()

    @classmethod
    def get_seller_comments(cls, seller_id):
        return cls.query.filter_by(comment_place_id=seller_id).all()

    def save_to_db(self):
        self.comment_id = self.generate_unique_id()
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
