from db import db


class Seller(db.Model):
    __tablename__ = "sellers"

    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(400), nullable=False, unique=True)  # we might discard this
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)

    # Add Seller-specific attributes here
    shop_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    total_rating = db.Column(db.Integer)
    total_raters = db.Column(db.Integer)
    directions = db.Column(db.String(400), nullable=False)

    # Define a one-to-many relationship between Seller and Product
    products = db.relationship('Product', back_populates='seller')

    @classmethod
    def find_by_unique_id(cls, unique_id):
        return cls.query.filter_by(unique_id=unique_id).first()

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
