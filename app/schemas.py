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
        fields.Dict(keys=fields.String() ,values=fields.String() | fields.List(fields.String()))
        )