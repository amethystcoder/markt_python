from marshmallow import Schema, fields


class ExampleSchema(Schema):
    message = fields.String()

class ProductSchema(Schema):
    id = fields.Int(strict=True)
    seller_id = fields.String()
    name = fields.String()
    description = fields.String()
    price = fields.Float()
    stock_quantity = fields.Int(strict=True)
    category = fields.String()
    #product_image = db.Column(db.String(400), nullable=False)
    
class CategorySchema:
    name = fields.String()
    tags = fields.List(
        fields.Dict(keys=fields.String() ,values=fields.String() or fields.List(fields.String()))
        )
    
class CartSchema:
    cart_id = fields.String()
    buyer_id = fields.String()
    product_id = fields.String()
    quantity = fields.Int(strict = True)
    has_discount = fields.Bool()
    discount_price = fields.Float()
    discount_percent = fields.Float()
    #order_status = db.Column(db.String(255), default='pending')