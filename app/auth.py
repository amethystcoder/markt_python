from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_login import login_user, logout_user, login_required, current_user

from .schemas import BuyerSchema, SellerSchema, UserSchema
from .models import User, Buyer, Seller

from .utils import ImageSaver
from .models.imagename_store_model import ImageNameStore
import tempfile

auth_blp = Blueprint("Auth", "auth", description="Endpoint for all API calls related to user authentication",
                     url_prefix="/auth")


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
