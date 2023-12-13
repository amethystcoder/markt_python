from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_login import login_user, logout_user, login_required, current_user

from .schemas import BuyerSchema, SellerSchema, UserSchema, UserRegisterSchema
from .models import User, Buyer, Seller, UserAddress

from .utils import ImageSaver
from .models.imagename_store_model import ImageNameStore
import tempfile

auth_blp = Blueprint("auth", __name__, description="Endpoint for all API calls related to user authentication",
                     url_prefix="/auth")


@auth_blp.route("/register")
class UserRegister(MethodView):
    @auth_blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        existing_user = User.query.filter_by(email=user_data["email"]).first()
        if existing_user:
            abort(409, message="A user with that email already exists.")

        new_user = User(
            email=user_data["email"],
            phone_number=user_data.get("phone_number"),
            password=user_data["password"],
            profile_picture=user_data.get("profile_picture")
        )

        role = user_data['role']

        if role == 'buyer':
            new_user.is_buyer = True
            new_user.save_to_db()

            new_buyer = Buyer(
                user_id=new_user.id, username=user_data["username"],
                shipping_address=user_data.get("shipping_address")
            )
            new_buyer.save_to_db()

        elif role == 'seller':
            new_user.is_seller = True
            new_user.save_to_db()

            new_seller = Seller(
                user_id=new_user.id,
                username=user_data["username"],
                store_name=user_data["store_name"],
                # continue later
            )
            new_user.save_to_db()

        else:
            abort(400, message="Invalid role")

        if 'address' in user_data:
            address_data = user_data['address']
            shipping_address = UserAddress(
                house_number=address_data.get('house_number'),
                street=address_data.get('street'),
                city=address_data.get('city'),
                state=address_data.get('state'),
                postal_code=address_data.get('postal_code')
            )
            new_user.shipping_address = shipping_address

        return {"message": "User created successfully."}, 201


@auth_blp.route("/buyer/register")
class BuyerRegistration(MethodView):
    @auth_blp.arguments(BuyerSchema)
    @auth_blp.response(201, description="User created successfully.")
    def post(self, data):
        pass


@auth_blp.route("/seller/register")
class SellerRegistration(MethodView):
    @auth_blp.arguments(SellerSchema)
    @auth_blp.response(201, description="User created successfully.")
    def post(self, data):
        pass


@auth_blp.route("/login")
class UserLogin(MethodView):
    @auth_blp.arguments(UserSchema(only=("username", "password")))
    @auth_blp.response(200, description="User logged in successfully.")
    def post(self, user_data):
        pass


@auth_blp.route("/logout")
class UserLogout(MethodView):
    @login_required # Protect this route
    @auth_blp.response(200, description="Logged out successfully")
    def post(self):
        pass
