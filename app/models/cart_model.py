from db import db
import hashlib
import uuid


class Cart(db.Model):
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cart_id = db.Column(db.String(400), nullable=False)
    buyer_id = db.Column(db.String(400), db.ForeignKey('buyers.unique_id'), nullable=False)
    product_id = db.Column(db.String(400), db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    has_discount = db.Column(db.Boolean, nullable=False)
    discount_price = db.Column(db.Float, nullable=False)
    discount_percent = db.Column(db.Float, nullable=False)
    #order_status = db.Column(db.String(255), default='pending')

    # Define relationships
    buyer = db.relationship("Buyer", back_populates="cart")
    product = db.relationship("Product", back_populates="cart")
    
    
    def __init__(self,buyer_id,product_id,quantity,has_discount,discount_price,discount_percent,cart_id):
        super().__init__()
        if cart_id is not None:
            self = Cart.get_buyer_cart_item(cart_id=cart_id)
        else:
            self.buyer_id = buyer_id
            self.product_id = product_id
            self.quantity = quantity
            self.has_discount = has_discount
            self.discount_price = discount_price
            self.discount_percent = discount_percent
    
    @classmethod
    def get_buyer_cart_items(self,buyer_id):
        return db.session.query(Cart).filter(Cart.buyer_id == buyer_id).all()
    
    @classmethod
    def get_buyer_cart_item(self,cart_id):
        return db.session.query(Cart).filter(Cart.cart_id == cart_id).first()
    
    def update_cart_quantity(self,newquantity):
        self.quantity = newquantity
        db.session.commit()
        
    @classmethod
    def delete_all_buyer_cart_items(self,buyer_id):
        return db.session.query(Cart).filter(Cart.buyer_id == buyer_id).delete()
    
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
