from db import db
import random

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.String(255), nullable=False)
    seller_id = db.Column(db.String(255), db.ForeignKey('sellers.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(255), nullable=False)
    product_image = db.Column(db.String(400), nullable=False)

    # Define a many-to-one relationship between Product and Seller
    seller = db.relationship('Seller', back_populates='products')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    def get_random_products(self,bundle_size):
        '''
        gets random products in a particular bundle based on the bundle size
        '''
        num_of_products = db.session.query(Product).count()
        random_ids = random.sample(range(1,num_of_products),bundle_size)
        return db.session.query(Product).filter(Product.id.in_(random_ids))
    
    def get_product_using_id(self,product_id):
        return db.session.query(Product).filter(Product.product_id == product_id)
    
    def create_product():
        pass
    
    def update_product():
        pass
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
