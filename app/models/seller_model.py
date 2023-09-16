from db import db


class Seller(db.Model):
    __tablename__ = "sellers"

    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(400), nullable=False, unique=True)
    shop_name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    total_rating = db.Column(db.Integer, nullable=False)
    total_raters = db.Column(db.Integer, nullable=False)
    directions = db.Column(db.String(400), nullable=False)
    profile_image = db.Column(db.String(400), nullable=False)
    house_number = db.Column(db.Integer, nullable=False)
    street = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.Integer, nullable=False)

    # Define a one-to-many relationship between Seller and Product
    products = db.relationship('Product', back_populates='seller')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
