from flask_smorest import Blueprint
from flask.views import MethodView
from flask_login import login_required

from ..schemas import BuyerSchema, SellerSchema, UserSchema, UserProfileSchema
from ..models import User

user_blp = Blueprint("users", __name__, description="Endpoint for all API calls related to users", url_prefix="/user")


@user_blp.route("/<int:user_id>")
class UserResource(MethodView):
    @login_required  # Protect this route
    @user_blp.response(200, UserSchema)
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user

    def post(self, user_id):
        pass

    def put(self, user_id):
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
