from db import db
import hashlib
import uuid


class Cart(db.Model):
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.String(400), nullable=False)
    # buyer_id = db.Column(db.String(400), db.ForeignKey('buyers.unique_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    has_discount = db.Column(db.Boolean, nullable=False)
    discount_price = db.Column(db.Float, nullable=False)
    discount_percent = db.Column(db.Float, nullable=False)
    # order_status = db.Column(db.String(255), default='pending')

    # Define buyer relationship
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyers.id'), nullable=False)
    buyer = db.relationship('Buyer', back_populates='carts')

    # Define product relationship
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship("Product", back_populates="carts")

    @classmethod
    def get_buyer_cart_items(cls, buyer_id):
        return cls.query.filter_by(buyer_id=buyer_id).all()

    @classmethod
    def get_buyer_cart_item(cls, cart_id):
        return cls.query.filter_by(cart_id=cart_id).first()

    def update_cart_quantity(self, new_quantity):
        self.quantity = new_quantity
        db.session.commit()

    @classmethod
    def delete_all_buyer_cart_items(cls, buyer_id):
        return cls.query.filter_by(buyer_id=buyer_id).delete()

    @staticmethod
    def generate_unique_id():
        unique_id = str(uuid.uuid4()).encode()
        return hashlib.sha256(unique_id).hexdigest()

    def save_to_db(self):
        self.cart_id = self.generate_unique_id()
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
