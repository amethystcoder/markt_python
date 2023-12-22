from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_login import login_required, current_user

from ..schemas import (
    BuyerSchema,
    BuyerUpdateSchema,
    SellerSchema,
    SellerUpdateSchema,
    UserSchema,
    UserProfileSchema,
    RoleArgSchema,
    UserProfileUpdateSchema
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
            }, 200

        abort(404, message="Seller not found")

    @login_required
    @user_blp.arguments(SellerUpdateSchema)
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
    @user_blp.arguments(RoleArgSchema)
    @user_blp.response(200, UserProfileSchema)
    def get(self, user_data):
        role = user_data.get('role', None)  # 'buyer', 'seller', or None for current role

        if role == 'buyer' and current_user.is_buyer:
            buyer = Buyer.query.filter_by(user_id=current_user.id).first()
            if buyer:
                buyer_info = {
                    "username": buyer.username,
                    "email": current_user.email,
                    "phone_number": current_user.phone_number or None,
                    "profile_picture": buyer.profile_picture,
                    "shipping_address": buyer.shipping_address
                }
                return UserProfileSchema.dump_buyer_info(buyer_info), 200
            else:
                abort(404, message="Buyer not found")

        elif role == 'seller' and current_user.is_seller:
            seller = Seller.query.filter_by(user_id=current_user.id).first()
            if seller:
                seller_info = {
                    "username": seller.username,
                    "email": current_user.email,
                    "profile_picture": seller.profile_picture,
                    "shop_name": seller.shop_name,
                    "description": seller.description,
                    "directions": seller.directions,
                    "category": seller.category,
                    "total_rating": seller.total_rating,
                    "total_raters": seller.total_raters,
                }
                return UserProfileSchema.dump_seller_info(seller_info), 200
            else:
                abort(404, message="Seller not found")
                
        else:
            # Return user information based on the current role
            if current_user.is_buyer:
                buyer = Buyer.query.filter_by(user_id=current_user.id).first()
                if buyer:
                    buyer_info = {
                        "username": buyer.username,
                        "email": current_user.email,
                        "phone_number": current_user.phone_number or None,
                        "profile_picture": buyer.profile_picture,
                        "shipping_address": buyer.shipping_address
                    }
                    return UserProfileSchema.dump_buyer_info(buyer_info), 200
            elif current_user.is_seller:
                seller = Seller.query.filter_by(user_id=current_user.id).first()
                if seller:
                    seller_info = {
                        "username": seller.username,
                        "email": current_user.email,
                        "profile_picture": seller.profile_picture,
                        "shop_name": seller.shop_name,
                        "description": seller.description,
                        "directions": seller.directions,
                        "category": seller.category,
                        "total_rating": seller.total_rating,
                        "total_raters": seller.total_raters,
                    }
                    return UserProfileSchema.dump_seller_info(seller_info), 200

        return abort(404, message="User profile not found")

    @login_required
    @user_blp.arguments(UserProfileUpdateSchema, user=current_user)
    @user_blp.response(200, description="Profile updated successfully")
    def put(self, user_data, user):
        # Validate user_data based on user's role, and update the profile accordingly
        if user.is_buyer:
            # Update buyer-related info
            buyer = Buyer.query.filter_by(user_id=user.id).first()
            buyer_info = user_data.get('buyer_info', {})

            if buyer_info:
                # Update buyer information based on the data received
                buyer.username = buyer_info.get("username", buyer.username)
                buyer.shipping_address = buyer_info.get("shipping_address", buyer.shipping_address)
                buyer.save_to_db()

        elif user.is_seller:
            # Update seller-related info
            seller = Seller.query.filter_by(user_id=user.id).first()
            seller_info = user_data.get('seller_info', {})

            if seller_info:
                # Update seller information based on the data received
                seller.username = user_data.get("username", seller.username)
                seller.shop_name = user_data.get("shop_name", seller.shop_name)
                seller.save_to_db()

        # We can do logic for updating common user info

        # Return a response as needed
        return {"message": "Profile updated successfully"}, 200
