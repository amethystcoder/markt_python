from flask_smorest import Blueprint
from flask.views import MethodView
from flask import abort, request
from ..schemas import BuyerSchema,SellerSchema
from .image_resizer_and_uploader import ImageSaver
from ..models.imagename_store_model import ImageNameStore
from ..models.user_model import User
from ..models.buyer_model import Buyer
from ..models.seller_model import Seller
import tempfile

user_bp = Blueprint("users", "user", description="Endpoint for all API calls related to users", url_prefix="/users")

@user_bp.route("/buyer/create")
class CreateBuyer(MethodView):
    @user_bp.arguments(BuyerSchema)
    @user_bp.response(201, BuyerSchema)
    def post(self,data):
        pass
    
@user_bp.route("/seller/create")
class CreateSeller(MethodView):
    @user_bp.arguments(SellerSchema)
    @user_bp.response(201, SellerSchema)
    def post(self,data):
        pass