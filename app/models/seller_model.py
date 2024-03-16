from db import db
from passlib.hash import pbkdf2_sha256


class Seller(db.Model):
    __tablename__ = "sellers"

    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(400), nullable=False, unique=True)  # we might discard this
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    profile_picture = db.Column(db.String(200))

    user_status = db.Column(db.String(255), default='active')

    # Add Seller-specific attributes here
    shop_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    total_rating = db.Column(db.Integer)
    total_raters = db.Column(db.Integer)
    directions = db.Column(db.String(400)) 

    # Define a one-to-many relationship between Seller and Product
    products = db.relationship('Product', back_populates='seller')
    orders = db.relationship("Order", back_populates="seller")
    comments = db.relationship("Comments", back_populates="seller")

    # Define favorites relationship (many-to-many)
    favorites = db.relationship('Favorite', secondary='favorites_seller_product', back_populates='sellers')

    # Define buyer_request relationship (many-to-many)
    buyer_requests = db.relationship('BuyerRequest', secondary='seller_buyer_query', back_populates='sellers')

    @classmethod
    def find_by_unique_id(cls, unique_id):
        return cls.query.filter_by(unique_id=unique_id).first()

    def set_password(self, password):
        self.password = pbkdf2_sha256.hash(password)

    def change_password(self, password):
        self.password = pbkdf2_sha256.hash(password)
        db.session.commit()

    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)

    def change_status(self, status):
        acceptable_status = ["active", "offline",
                             "standby"]  # standby could be a status for when user is online but not on present screen
        if status in acceptable_status:
            self.user_status = status
            db.session.commit()

    def update_rating(self, rating):
        self.total_raters = self.total_raters + 1
        self.total_rating = self.total_rating + rating
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # Add Seller-specific methods here
