from db import db
import random
import hashlib
import uuid


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.String(255), nullable=False)
    # seller_id = db.Column(db.String(255), db.ForeignKey('sellers.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(255), nullable=False)

    # Define seller relationship
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'), nullable=False)
    seller = db.relationship('Seller', back_populates='products')

    # Define relationships (one-many)
    cart = db.relationship("Cart", back_populates="product")
    comments = db.relationship("Comments", back_populates="product")
    image_name_store = db.relationship('ImageNameStore', back_populates='product')

    # Define relationships (many-to-many)
    favorites = db.relationship('Favorite', secondary='favorites_seller_product', back_populates='products')
    orders = db.relationship('Order', secondary='products_orders', back_populates='products')

    """
    def __init__(self, seller_id, name, description, price, stock_quantity, category, product_id):
        if product_id:
            self = self.get_product_using_id(product_id)
        else:
            self.seller_id = seller_id
            self.name = name
            self.description = description
            self.price = price
            self.stock_quantity = stock_quantity
            self.category = category
    """

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_random_products(cls, bundle_size):
        """
        gets random products in a particular bundle based on the bundle size
        """
        try:
            num_of_products = cls.query.count()
            random_ids = random.sample(range(1, num_of_products), int(bundle_size))
            return cls.query.filter_by(id=random_ids).all()
        except ValueError:
            return []

    @staticmethod
    def generate_unique_id():
        unique_id = str(uuid.uuid4()).encode()
        return hashlib.sha256(unique_id).hexdigest()

    @classmethod
    def get_product_using_id(cls, product_id):
        return cls.query.filter_by(id=product_id).first()

    @classmethod
    def get_products_using_seller_id(cls, seller_id):
        return cls.query.filter_by(seller_id=seller_id).all()

    @classmethod
    def search_product_using_name(cls, product_name):
        return cls.query.filter_by(cls.name.like(f"%{product_name}%")).all()

    @classmethod
    def search_product_using_category(cls, category_name):
        return cls.query.filter_by(cls.name.like(f"%{category_name}%")).all()

    def set_product_id(self):
        self.product_id = self.generate_unique_id()

    def update_product(self, product_data):
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
