from db import db
import time
import hashlib
import uuid


class BuyerRequest(db.Model):
    __tablename__ = "buyer_request"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unique_id = db.Column(db.String(400), nullable=False)
    buyer_id = db.Column(db.String(400), db.ForeignKey('buyers.unique_id'), nullable=False)
    product_description = db.Column(db.String(400), nullable=False)
    category = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP, default=time.time(), nullable=False)
    status = db.Column(db.String(255), default="open")

    buyer = db.relationship("Buyer", back_populates="requests")

    """
    def __init__(self, buyer_id, product_description, category, unique_id):
        if unique_id is not None:
            self = self.get_requests_through_id(unique_id)
        else:
            self.unique_id = self.generate_unique_id()
            self.buyer_id = buyer_id
            self.product_description = product_description
            self.category = category
    """

    @staticmethod
    def generate_unique_id():
        unique_id = str(uuid.uuid4()).encode()
        return hashlib.sha256(unique_id).hexdigest()

    @classmethod
    def get_requests_through_id(cls, _id):
        return cls.query.filter_by(unique_id=_id).all()

    @classmethod
    def get_requests_through_buyer_id(cls, buyer_id):
        return cls.query.filter_by(buyer_id=buyer_id).all()

    @classmethod
    def get_requests_using_category(cls, *args):
        return cls.query.filter_by(cls._in(list(args))).all()

    @classmethod
    def delete_all_buyer_requests(cls, buyer_id):
        return cls.query.filter_by(buyer_id=buyer_id).delete()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
