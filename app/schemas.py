from marshmallow import Schema, fields, validate, post_load


class ExampleSchema(Schema):
    message = fields.String()


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    phone_number = fields.Str()
    profile_picture = fields.Str()


class BuyerSchema(UserSchema):
    password = fields.Str(required=True, load_only=True)
    shipping_address = fields.Str(required=True)  # We haven't thought of any buyer specific attr


class SellerSchema(UserSchema):
    password = fields.Str(required=True, load_only=True)
    shop_name = fields.Str(required=True)
    description = fields.Str(required=True)
    directions = fields.String(required=True)
    category = fields.String(required=True)


class AddressSchema(Schema):
    longitude = fields.Float()
    latitude = fields.Float()
    house_number = fields.Int()
    street = fields.String()
    city = fields.String()
    state = fields.String()
    country = fields.String()
    postal_code = fields.Int()


class UserRegisterSchema(Schema):
    role = fields.Str(validate=validate.OneOf(["buyer", "seller"]), required=True)
    address = fields.Nested(AddressSchema, required=False)

    @post_load
    def process_role(self, data, **kwargs):
        role = data.get('role')
        if role == 'buyer':
            return BuyerSchema().load(data)
        elif role == 'seller':
            return SellerSchema().load(data)
        return data


class RoleSchema(Schema):
    is_buyer = fields.Bool()
    is_seller = fields.Bool()


class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    account_type = fields.Str(required=True)


class UserLoginResponseSchema(Schema):
    message = fields.Str()
    role = fields.Nested(RoleSchema)


class UserProfileSchema(Schema):
    pass


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


class CommentSchema:
    id = fields.Int(strict=True)
    comment_id = fields.String()
    comment_title = fields.String()
    buyer_id = fields.String()
    buyer_name = fields.String()
    comment_place_id = fields.String()  # the id of the place the comment is created
    comment_date = fields.DateTime()


class FavoriteSchema:
    id = fields.Int(strict=True)
    buyer_id = fields.String()
    favorite_item_id = fields.String()  # the id of the buyer favorite (seller or product)
    favorite_type = fields.String()  # seller or product
