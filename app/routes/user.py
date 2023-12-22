from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_login import login_required, current_user

from ..schemas import (
    BuyerSchema,
    BuyerUpdateSchema,
    SellerSchema,
    SellerUpdateSchema,
    UserSchema,
    UserProfileSchema
)
from ..models import User, Buyer, Seller

user_blp = Blueprint("users", __name__, description="Endpoint for all API calls related to users", url_prefix="/user")


@user_blp.route("/<int:user_id>")
class UserResource(MethodView):
    # functions here are used for testing
    @login_required  # Protect this route
    @user_blp.response(200, UserSchema)
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user

    def post(self, user_id):
        pass

    def put(self, user_id):
        pass


@user_blp.route("/buyer")
class BuyerResource(MethodView):
    @login_required
    @user_blp.response(200, BuyerSchema)
    def get(self):
        buyer_info = Buyer.query.filter_by(user_id=current_user.id).first()
        if buyer_info:
            return {
                "username": buyer_info.username,
                "email": current_user.email,
                "phone_number": current_user.phone_number or None,
                "profile_picture": buyer_info.profile_picture,
                "shipping_address": buyer_info.shipping_address
            }, 200
        abort(404, message="Buyer not found")

    @login_required
    @user_blp.arguments(BuyerUpdateSchema)
    @user_blp.response(200, description="Buyer profile updated successfully.")
    def put(self, user_data):
        buyer_info = Buyer.query.filter_by(user_id=current_user.id).first()
        if buyer_info:
            # Update buyer information based on the data received
            buyer_info.username = user_data.get("username", buyer_info.username)
            buyer_info.shipping_address = user_data.get("shipping_address", buyer_info.shipping_address)
            buyer_info.save_to_db()
            return {"message": "Buyer profile updated successfully."}, 200

        abort(404, message="Buyer not found")

    def delete(self):
        #  Deletion considerations TBD
        pass


@user_blp.route("/seller")
class SellerResource(MethodView):
    @login_required
    @user_blp.response(200, SellerSchema)
    def get(self):
        seller_info = Seller.query.filter_by(user_id=current_user.id).first()
        if seller_info:
            return {
                "username": seller_info.username,
                "email": current_user.email,
                "profile_picture": seller_info.profile_picture,
                "shop_name": seller_info.shop_name,
                "description": seller_info.description,
                "directions": seller_info.directions,
                "category": seller_info.category,
                "total_rating": seller_info.total_rating,
                "total_raters": seller_info.total_raters,
            }

        abort(404, message="Seller not found")

    @login_required
    @user_blp.arguments(BuyerUpdateSchema)
    @user_blp.response(200, description="Seller profile updated successfully.")
    def put(self, user_data):
        seller_info = Seller.query.filter_by(user_id=current_user.id).first()
        if seller_info:
            # Update seller information based on the data received
            seller_info.username = user_data.get("username", seller_info.username)
            seller_info.shop_name = user_data.get("shop_name", seller_info.shop_name)
            seller_info.save_to_db()
            return {"message": "Seller profile updated successfully."}, 200

        abort(404, message="Seller not found")

    def delete(self):
        #  Deletion considerations TBD
        pass


@user_blp.route("/profile")
class UserProfile(MethodView):
    @login_required
    @user_blp.response(200, UserProfileSchema)
    def get(self):
        pass

    @login_required
    @user_blp.arguments(UserProfileSchema(partial=True))
    @user_blp.response(200, UserProfileSchema)
    def put(self, user_data):
        pass
