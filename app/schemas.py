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
    # product_image = fields.String()

class CategorySchema:
    name = fields.String()
    tags = fields.List(
        fields.Dict(keys=fields.String(), values=fields.String() or fields.List(fields.String()))
    )

class CartSchema:
    cart_id = fields.String()
    buyer_id = fields.String()
    product_id = fields.String()
    quantity = fields.Int(strict=True)
    has_discount = fields.Bool()
    discount_price = fields.Float()
    discount_percent = fields.Float()
    # order_status = db.Column(db.String(255), default='pending')

class ProductRequestSchema:
    buyer_id = fields.String()
    product_description = fields.String()
    category = fields.String()
    created_at = fields.DateTime()
    status = fields.String()

class PasswordRetrievalSchema:
    id = fields.Int(strict=True)
    recovery_code = fields.Int(strict=True)
    user_id = fields.String()
    email = fields.String()
    expiration_time = fields.Int(strict=True)

class OrderSchema:
    id = fields.Int(strict=True)
    buyer_id = fields.String()
    seller_id = fields.String()
    product_id = fields.String()
    quantity = fields.Int(strict=True)
    total_price = fields.Float()
    order_status = fields.String()
    order_date = fields.DateTime()
    delivery_address = fields.String()

class BuyerSchema:
    id = fields.Int(strict=True)
    username = fields.String()
    unique_id = fields.String()
    email = fields.String()
    password = fields.String()
    profile_picture = fields.String()
    phone_number = fields.String()
    longitude = fields.Float()
    latitude = fields.Float()
    house_number = fields.Int()
    street = fields.String()
    city = fields.String()
    state = fields.String()
    country = fields.String()
    postal_code = fields.Int()
    user_type = fields.String()
    user_status = fields.String()

class SellerSchema:
    id = fields.Int(strict=True)
    shop_name = fields.String()
    description = fields.String()
    category = fields.String()
    seller_rating = fields.Float()
    directions = fields.String()
    unique_id = fields.String()
    email = fields.String()
    password = fields.String()
    profile_picture = fields.String()
    phone_number = fields.String()
    longitude = fields.Float()
    latitude = fields.Float()
    house_number = fields.Int()
    street = fields.String()
    city = fields.String()
    state = fields.String()
    country = fields.String()
    postal_code = fields.Int(strict=True)
    user_type = fields.String()
    user_status = fields.String()
    
class CommentSchema:
    id = fields.Int(strict=True)
    comment_id = fields.String()
    comment_title = fields.String()
    buyer_id = fields.String()
    buyer_name = fields.String()
    comment_place_id = fields.String() #the id of the place the comment is created
    comment_date = fields.DateTime()
    
class FavoriteSchema:
    id = fields.Int(strict=True)
    buyer_id = fields.String()
    favorite_item_id = fields.String() #the id of the buyer favorite (seller or product)
    favorite_type = fields.String() #seller or product