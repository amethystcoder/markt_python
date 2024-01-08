from db import db
import random
import hashlib
import uuid

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

    # Define a many-to-one relationship between Product and Seller
    seller = db.relationship('Seller', back_populates='products')
    
    imagenamestore = db.relationship('ImageNameStore', back_populates='products')
    
    def __init__(self,seller_id,name,description,price,stock_quantity,category,product_id):
        if product_id:
            self = self.get_product_using_id(product_id)
        else:
            self.seller_id = seller_id
            self.name = name
            self.description = description
            self.price = price
            self.stock_quantity = stock_quantity
            self.category = category
        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()    
    
    @classmethod
    def get_random_products(self,bundle_size):
        '''
        gets random products in a particular bundle based on the bundle size
        '''
        try:
            num_of_products = db.session.query(Product).count()
            random_ids = random.sample(range(1,num_of_products),int(bundle_size))
            return db.session.query(Product).filter(Product.id.in_(random_ids)).all()
        except ValueError:
            return []
    
    def generate_unique_id():
        unique_id = str(uuid.uuid4()).encode()
        return hashlib.sha256(unique_id).hexdigest()
    
    @classmethod
    def get_product_using_id(self,product_id):
        return db.session.query(Product).filter(Product.product_id == product_id).first()
    
    @classmethod
    def get_products_using_sellerid(self,seller_id):
        return db.session.query(Product).filter(Product.seller_id == seller_id).all()
    
    @classmethod
    def search_product_using_name(self,product_name):
        return db.session.query(Product).filter(Product.name.like("%"+product_name+"%")).all()
    
    @classmethod
    def search_product_using_category(self,category_name):
        return db.session.query(Product).filter(Product.category.like("%"+category_name+"%")).all()
    
    def setproductid(self):
        self.product_id = self.generate_unique_id()
    
    def update_product(self,product_data):
        """updates part or all of the current map/session of self(present class)
    
            only name,description,price,stock_quantity and category can be updated
        """
        try:
            if product_data["name"] is not None and type(product_data["name"]) == str:
                self.name = product_data["name"]
            if product_data["description"] is not None and type(product_data["description"]) == str:
                self.description = product_data["description"]
            if product_data["price"] is not None and type(product_data["price"]) == str:
                self.price = product_data["price"]
            if product_data["stock_quantity"] is not None and type(product_data["stock_quantity"]) == str:
                self.stock_quantity = product_data["stock_quantity"]
            if product_data["category"] is not None and type(product_data["category"]) == str:
                self.category = product_data["category"]
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
