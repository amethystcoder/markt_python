from db import db

class Buyer(db.Model):
    __tablename__ = "buyers"

    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(400), nullable=False, unique=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    profile_image = db.Column(db.String(400), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    house_number = db.Column(db.Integer, nullable=False)
    street = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.Integer, nullable=False)
    user_type = db.Column(db.String(255), nullable=False)
    user_status = db.Column(db.String(255), default='active')

    # Define a one-to-many relationship between Buyer and Order
    orders = db.relationship('Order', back_populates='buyer')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
