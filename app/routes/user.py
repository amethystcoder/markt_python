from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_login import login_user, logout_user, login_required, current_user

from ..schemas import BuyerSchema, SellerSchema, UserSchema
from ..models import User, Buyer, Seller

from .image_resizer_and_uploader import ImageSaver
from ..models.imagename_store_model import ImageNameStore
import tempfile

user_blp = Blueprint("users", "user", description="Endpoint for all API calls related to users", url_prefix="/users")


@user_blp.route("/user/<int:user_id>")
class UserResource(MethodView):
    @jwt_required()  # Protect this route with JWT
    @user_blp.response(200, UserSchema)
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user

    def post(self, user_id):
        pass

    def put(self, user_id):
        pass


@user_blp.route("/buyer/create")
class CreateBuyer(MethodView):
    @user_blp.arguments(BuyerSchema)
    @user_blp.response(201, BuyerSchema)
    def post(self, data):
        pass


@user_blp.route("/seller/create")
class CreateSeller(MethodView):
    @user_blp.arguments(SellerSchema)
    @user_blp.response(201, SellerSchema)
    def post(self, data):
        pass
