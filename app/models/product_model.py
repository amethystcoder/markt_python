from db import db
from sqlalchemy.sql import func
import uuid


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(400), nullable=False, unique=True)
    product_name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    stock = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)

    # Define seller relationship
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'), nullable=False)
    seller = db.relationship('Seller', back_populates='products')

    # Define buyer requests relationship
    buyer_requests = db.relationship('BuyerRequest', back_populates='product')

    # Define favorites relationship
    favorites = db.relationship('Favorite', back_populates='product')

    # Define comments relationship
    comments = db.relationship('Comments', back_populates='product')

    @staticmethod
    def generate_unique_id():
        return str(uuid.uuid4())

    @classmethod
    def get_product_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_products_by_seller_id(cls, seller_id):
        return cls.query.filter_by(seller_id=seller_id).all()

    def save_to_db(self):
        if not self.product_id:
            self.product_id = self.generate_unique_id()
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_from_db(self):
        db.session.delete(self)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
