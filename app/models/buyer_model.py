from db import db
from passlib.hash import pbkdf2_sha256


class Buyer(db.Model):
    __tablename__ = "buyers"

    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(400), nullable=False, unique=True)  # we might discard this
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    profile_picture = db.Column(db.String(200))

    user_status = db.Column(db.String(255), default='active')

    # Add Buyer-specific attributes here
    shipping_address = db.Column(db.String(255), nullable=True)  # just for test

    # Define one-many relationship
    carts = db.relationship('Cart', back_populates='buyer')
    favorites = db.relationship('Favorite', back_populates='buyer')
    buyer_requests = db.relationship('BuyerRequest', back_populates="buyer")
    orders = db.relationship("Order", back_populates="buyer")
    comments = db.relationship("Comments", back_populates="buyer")

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

    def save_to_db(self):
        self.unique_id = self.generate_unique_id()
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # Add Buyer-specific methods here
