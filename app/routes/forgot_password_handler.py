from flask_smorest import Blueprint
from flask.views import MethodView
from flask import abort
import random
from app import mail
from flask_mail import Message

from ..models import PasswordRetrievalData, User
from app.schemas import PasswordRetrievalSchema

pswd_retrvl_bp = Blueprint("Retrieve Password", "retrieve password", description="Endpoint for password retrieval")


@pswd_retrvl_bp.route("/create")
class PasswordRetrival(MethodView):
    @pswd_retrvl_bp.response(201, PasswordRetrievalSchema)
    def post(self, data):
        try:
            PasswordRetrievalData.delete_all_other_recovery_attempts(data["email"])
            ret_code = random.randint(100000, 999999)
            new_password_retrieval = PasswordRetrievalData(data["user_id"], data["email"], ret_code)
            new_password_retrieval.save_to_db()
            msg = Message(subject='Psst, Your Password Retrieval Code',
                          sender='',
                          recipients=[''])
            msg.body = f"Hey there. We heard you forgot your password. Let's try to get you back in. Here is your verification code. {ret_code} Enter this code into the website to get back into your account and continue your transactions P.S: This code expires in three minutes. If you did not request for this code, please ignore this mail and change your password as some one might have gotten access to your passwordDo not reply this message as you will not receive any response."
            msg.html = f"<div> <h2>Hey there.</h2> <p>we heard you forgot your password. Let's try to get you back in. Here is your verification code.</p> <h1 style='display:flex;justify-content:center;align-items:center'> {ret_code} </h1> <p>Enter this code into the website to get back into your account and continue your transactions</p> <p>P.S: This code expires in three minutes.</p> <p>If you did not request for this code, please ignore this mail and change yourpassword as some one might have gotten access to your password</p> <p>Do not reply this message as you will not receive any response.</p> <div>"
            mail.send(msg)
        except Exception as e:
            abort(500, "could not create")


@pswd_retrvl_bp.route("/check")
class PasswordCodeCheck(MethodView):
    @pswd_retrvl_bp.response(201, PasswordRetrievalSchema)
    def post(self, data):  # TODO: refactor this function
        try:
            password_retrieval_to_check = PasswordRetrievalData(email=data["email"])
            if password_retrieval_to_check.is_expired():
                abort()
            elif password_retrieval_to_check.is_code_right(code=data["code"]):
                user_to_update = User(email=data["email"], password_change_reset=True)  # TODO: TBD
                user_to_update.change_password(password=data["password"])
                password_retrieval_to_check.delete_all_other_recovery_attempts(email=data["email"])
        except Exception as e:
            abort(404, "not found")
