from db import db
import time



class BuyerRequest(db.Model):
    __tablename__ = "buyer_request"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unique_id =  db.Column(db.String(400), nullable=False)
    buyer_id = db.Column(db.String(400), db.ForeignKey('buyers.unique_id'), nullable=False)
    product_description = db.Column(db.String(400), nullable=False)
    category = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP, default=time.asctime(), nullable=False)
    status = db.Column(db.String(255), default="open")

    # Define relationship
    buyer = db.relationship("Buyer", back_populates="requests")
    
    def __init__(self,buyer_id,product_description,category):
        self.buyer_id = buyer_id
        self.product_description = product_description
        self.category = category
        

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
