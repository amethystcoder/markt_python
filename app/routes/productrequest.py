from flask_smorest import Blueprint
from flask.views import MethodView
from flask import abort
from app.schemas import ProductRequestSchema
from app.models import buyer_request_model

productrequest_bp = Blueprint("Product Request", "request", description="Api calls to buyer product request apis")


@productrequest_bp.route("/new")
class NewProductRequest(MethodView):
    @productrequest_bp.response(200, ProductRequestSchema)
    def post(self):
          try:
            pass
          except Exception as e:
            abort(500,"could not create request")
      
@productrequest_bp.route("/<unique-id>")
class ProductRequest(MethodView):
    @productrequest_bp.response(200, ProductRequestSchema)
    def get(self):

        return 
      
"""
These are just some functions that make api calls i copied from the client. 
I am using them to track and revise additions.

  createproductquery,
  getqueriesthroughcategory,
  getbuyerqueries,
  getsellerqueries,
"""