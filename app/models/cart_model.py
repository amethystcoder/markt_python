from db import db
import uuid


class Cart(db.Model):
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.String(400), nullable=False, unique=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyers.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    status = db.Column(db.String(255), default="pending")

    # Define buyer relationship
    buyer = db.relationship('Buyer', back_populates='carts')
    # Define product relationship
    product = db.relationship('Product', back_populates='carts')

    @staticmethod
    def generate_unique_id():
        return str(uuid.uuid4())

    @classmethod
    def get_cart_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_cart_by_buyer_id(cls, buyer_id):
        return cls.query.filter_by(buyer_id=buyer_id).all()

    def save_to_db(self):
        if not self.cart_id:
            self.cart_id = self.generate_unique_id()
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
