from db import db


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyers.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    order_status = db.Column(db.String(255), default='pending', nullable=False)
    order_date = db.Column(db.TIMESTAMP, nullable=False)
    delivery_address = db.Column(db.String(400), nullable=False)

    # Define a many-to-one relationship between Order and Buyer
    buyer = db.relationship('Buyer', back_populates='orders')

    # Define a many-to-one relationship between Order and Seller
    seller = db.relationship('Seller', back_populates='orders')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
