from db import db

sellers_orders = db.Table(
    'sellers_orders',
    db.Column('seller_id', db.Integer, db.ForeignKey('seller.id'), primary_key=True),
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True)
)
