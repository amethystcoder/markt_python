from db import db
from passlib.hash import pbkdf2_sha256
from flask_login import UserMixin
import hashlib
import uuid


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    profile_picture = db.Column(db.String(200))

    is_buyer = db.Column(db.Boolean, default=False)
    is_seller = db.Column(db.Boolean, default=False)
    user_status = db.Column(db.String(255), default='active')

    # Add other common attributes here

    # Define a relationship with the Chat model
    chats = db.relationship('Chat', back_populates='user')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def generate_unique_id():
        unique_id = str(uuid.uuid4()).encode()
        return hashlib.sha256(unique_id).hexdigest()

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

    @classmethod
    def get_user_location_data(cls, _id):
        data = UserAddress.query.filter_by(id=_id)
        return {
            "city": data.city,
            "country": data.country,
            "longitude": data.longitude,
            "latitude": data.latitude,
            "house_number": data.house_number,
            "state": data.state,
            "street": data.street,
            "postal_code": data.postal_code
        }


class UserAddress(db.Model):
    __tablename__ = "user_address"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    house_number = db.Column(db.Integer)
    street = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    country = db.Column(db.String(255))
    postal_code = db.Column(db.Integer)
