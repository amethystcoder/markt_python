from db import db


class Cart(db.Model):
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cart_id = db.Column(db.String(400), nullable=False)
    buyer_id = db.Column(db.String(400), db.ForeignKey('buyer.unique_id'), nullable=False)
    product_id = db.Column(db.String(400), db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    has_discount = db.Column(db.Boolean, nullable=False)
    discount_price = db.Column(db.Float, nullable=False)
    discount_percent = db.Column(db.Float, nullable=False)
    #order_status = db.Column(db.String(255), default='pending')

    # Define relationships
    buyer = db.relationship("Buyer", back_populates="cart_items")
    product = db.relationship("Product", back_populates="carts")
    
    
    def __init__(self,buyer_id ,product_id,quantity,has_discount,discount_price,discount_percent):
        super().__init__()
        self.buyer_id = buyer_id
        self.product_id = product_id
        self.quantity = quantity
        self.has_discount = has_discount
        self.discount_price = discount_price
        self.discount_percent = discount_percent
    
    def get_buyer_cart_items(self,buyer_id):
        return db.session.query(Cart).filter(Cart.buyer_id == buyer_id).all()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
