from flask_smorest import Blueprint
from flask.views import MethodView
from flask import abort
import random
from app.models.password_retrieval_store import PasswordRetrievalData
from app.models.user_model import User

from app.schemas import PasswordRetrievalSchema

pswd_retrvl_bp = Blueprint("Retrieve Password", "retrieve password", description="Endpoint for password retrieval")

@pswd_retrvl_bp.route("/create")
class PasswordRetrival(MethodView):
    @pswd_retrvl_bp(201, PasswordRetrievalSchema)
    def post(self,data):
        try:
            PasswordRetrievalData.delete_all_other_recovery_attempts(data["email"])
            ret_code = random.randint(100000,999999)
            new_password_retrieval = PasswordRetrievalData(data["user_id"],data["email"],ret_code)
            new_password_retrieval.save_to_db()
            #ADD FUNCTION HERE TO SEND CODE TO EMAIL
        except Exception as e:
            abort(500,"could not create")

@pswd_retrvl_bp.route("/check")
class PasswordCodeCheck(MethodView):
    @pswd_retrvl_bp(201, PasswordRetrievalSchema)
    def post(self,data):
        try:
            password_retrieval_to_check = PasswordRetrievalData(email=data["email"])
            if password_retrieval_to_check.is_expired():
                abort()
            elif password_retrieval_to_check.is_code_right(code=data["code"]):
                user_to_update = User(email=data["email"])
                user_to_update.change_password(password=data["password"])
                password_retrieval_to_check.delete_all_other_recovery_attempts(email=data["email"])
        except Exception as e:
            abort(404,"not found")