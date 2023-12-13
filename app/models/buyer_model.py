from db import db


class Buyer(db.Model):
    __tablename__ = "buyers"

    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(400), nullable=False, unique=True)  # we might discard this
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)

    # Add Buyer-specific attributes here

    @classmethod
    def find_by_unique_id(cls, unique_id):
        return cls.query.filter_by(unique_id=unique_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # Add Buyer-specific methods here
