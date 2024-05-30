from db import db
import time
import hashlib
import uuid


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unique_id = db.Column(db.String(400), nullable=False, unique=True)
    order_id = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    order_status = db.Column(db.String(255), default='pending', nullable=False)
    order_date = db.Column(db.TIMESTAMP, nullable=False)
    delivery_address = db.Column(db.String(400), nullable=False)

    # Define seller relationship
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'), nullable=False)
    seller = db.relationship('Seller', back_populates='orders')

    # Define buyer relationship
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyers.id'), nullable=False)
    buyer = db.relationship('Buyer', back_populates='orders')

    # Define product relationship (many-to-many)
    products = db.relationship('Product', secondary='products_orders', back_populates='orders')

    ''' def __repr__(self) -> str:
        return self
     '''

    """
    def __init__(self, buyer_id, seller_id, product_id, quantity, total_price, delivery_address, order_id):
        if order_id is None:
            self.buyer_id = buyer_id
            self.seller_id = seller_id
            self.product_id = product_id
            self.quantity = quantity
            self.total_price = total_price
            self.order_date = time.time()
            self.delivery_address = delivery_address
        else:
            self = self.get_order_using_id(order_id)
    """

    ''' def __eq__(self, __value: object) -> bool:
        return super().__eq__(__value) '''

    @classmethod
    def get_order_using_id(cls, order_id):
        return cls.query.filter_by(order_id=order_id).first()

    @classmethod
    def get_seller_pending_orders(cls, seller_id):
        return cls.query.filter_by(seller_id=seller_id, order_status='pending').all()

    @classmethod
    def get_seller_accepted_orders(cls, seller_id):
        return cls.query.filter_by(seller_id=seller_id, order_status='accepted').all()

    @classmethod
    def get_buyer_orders(cls, buyer_id):
        return cls.query.filter_by(buyer_id=buyer_id).all()

    @staticmethod
    def generate_unique_id():
        unique_id = str(uuid.uuid4()).encode()
        return hashlib.sha256(unique_id).hexdigest()

    def accept_order(self):
        self.order_status = "accepted"
        db.session.commit()

    def decline_order(self):
        self.order_status = "declined"
        db.session.commit()

    def save_to_db(self):
        self.order_id = self.generate_unique_id()
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
