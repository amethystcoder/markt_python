from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import and_

from .schemas import (
    BuyerSchema,
    SellerSchema,
    UserSchema,
    UserRegisterSchema,
    UserLoginSchema,
    UserLoginResponseSchema,
)
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

        existing_user = User.query.filter(
                and_(
                    User.email == user_data["email"],
                    User.phone_number == user_data["phone_number"],
                )
        ).first()
        if existing_user:
            has_buyer_account = Buyer.query.filter_by(user_id=existing_user.id).first()
            has_seller_account = Seller.query.filter_by(user_id=existing_user.id).first()
            # Check if the user already has the specified role
            if (
                    (user_data["role"] == 'buyer' and has_buyer_account) or
                    (user_data["role"] == 'seller' and has_seller_account)
            ):
                abort(409, message=f"User already has a {user_data['role']} account.")

        existing_username = (
                Buyer.query.filter_by(username=user_data["username"]).first() or
                Seller.query.filter_by(username=user_data["username"]).first()
        )
        if existing_username:
            abort(409, message="A user with that username already exists.")

        existing_email = User.query.filter_by(email=user_data["email"]).first()
        if existing_email:
            abort(409, message="A user with that email already exists.")

        existing_phone = User.query.filter_by(phone_number=user_data["phone_number"]).first() if user_data["phone_number"] else None
        if existing_phone:
            abort(409, message="A user with that phone number already exists.")

        new_user = User(
            email=user_data["email"],
            phone_number=user_data["phone_number"],
        )

        role = user_data['role']

        if role == 'buyer':
            new_user.is_buyer = True
            new_user.save_to_db()

            new_buyer = Buyer(
                user_id=new_user.id,
                username=user_data["username"],
                password=user_data["password"],
                profile_picture=user_data.get("profile_picture", "defaultThumbnailImageUrl"),
                shipping_address=user_data.get("shipping_address")
            )
            new_buyer.save_to_db()

        elif role == 'seller':
            new_user.is_seller = True
            new_user.save_to_db()

            new_seller = Seller(
                user_id=new_user.id,
                username=user_data["username"],
                password=user_data["password"],
                profile_picture=user_data.get("profile_picture", "defaultThumbnailImageUrl"),
                shop_name=user_data["shop_name"],
                description=user_data["description"],
                directions=user_data["directions"],
                category=user_data["category"]
            )
            new_seller.save_to_db()

        else:
            abort(400, message="Invalid role")

        if 'address' in user_data:
            address_data = user_data['address']
            user_address = UserAddress(
                house_number=address_data.get('house_number'),
                street=address_data.get('street'),
                city=address_data.get('city'),
                state=address_data.get('state'),
                postal_code=address_data.get('postal_code')
            )
            user_address.save_to_db()

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


@auth_blp.route("/switch-role")
class SwitchRole(MethodView):
    @login_required
    @auth_blp.response(200, description="User switched successfully.")
    def post(self):
        user = current_user
        if user.is_buyer:
            # Check if the user has an existing seller account before switching
            if Seller.query.filter_by(user_id=user.id).first() is None:
                abort(400, message="User does not have a seller account.")

            user.is_seller = True
            user.save_to_db()

        elif user.is_seller:
            # Check if the user has an existing buyer account before switching
            if Buyer.query.filter_by(user_id=user.id).first() is None:
                abort(400, message="User does not have a buyer account.")

            user.is_seller = True
            user.save_to_db()

        return {"message": "User switched successfully."}, 400


@auth_blp.route("/login")
class UserLogin(MethodView):
    @auth_blp.arguments(UserLoginSchema)
    @auth_blp.response(200, UserLoginResponseSchema)
    def post(self, user_data):
        email = user_data["email"]
        password = user_data["password"]
        account_type = user_data["account_type"]

        user = User.query.filter_by(email=email).first()
        buyer_account = Buyer.query.filter_by(user_id=user.id).first()
        seller_account = Seller.query.filter_by(user_id=user.id).first()

        if user and account_type == 'buyer' and buyer_account:
            if buyer_account.check_password(buyer_account.password, password):
                login_user(user)
                return {
                    "message": "Login successful",
                    "role": {
                        "is_buyer": user.is_buyer,
                        "is_seller": user.is_seller}
                }, 200

        elif user and account_type == 'seller' and seller_account:
            if seller_account.check_password(seller_account.password, password):
                login_user(user)
                return {
                    "message": "Login successful",
                    "role": {
                        "is_buyer": user.is_buyer,
                        "is_seller": user.is_seller}
                }, 200

        abort(401, message="Invalid credentials.")


@auth_blp.route("/logout")
class UserLogout(MethodView):
    @login_required  # Protect this route
    @auth_blp.response(200, description="Logged out successfully")
    def post(self):
        logout_user()
        return {"message": "Logged out successful"}, 200
