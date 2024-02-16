from db import db


class Payment(db.Model):
    __tablename__ = "payment"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    payment_id = db.Column(db.String(400), nullable=False)
    order_id = db.Column(db.String(400), db.ForeignKey('orders.id'), nullable=False)
    payment_method = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(255), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)

    # Define relationship
    # order = db.relationship("Order", back_populates="payments")

    def __init__(self):
        pass

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
