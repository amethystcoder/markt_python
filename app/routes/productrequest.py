from flask_smorest import Blueprint
from flask.views import MethodView
from flask import abort
from app.schemas import ProductRequestSchema
from app.models.buyer_request_model import BuyerRequest

productrequest_bp = Blueprint("Product Request", "request", description="Api calls to buyer product request apis")


@productrequest_bp.route("/new")
class NewProductRequest(MethodView):
    @productrequest_bp.response(200, ProductRequestSchema)
    def post(self,product_request_data):
          try:
            request = BuyerRequest(product_request_data["buyer_id"],product_request_data["product_description"],
                                  product_request_data["category"])
            request.save_to_db()
          except Exception as e:
            abort(500,"could not create request")
      
@productrequest_bp.route("/<unique-id>")
class ProductRequest(MethodView):
    @productrequest_bp.response(200, ProductRequestSchema)
    def get(self):

        return 
    
    def delete(self):
        return
      
@productrequest_bp.route("/<buyer_id>")
class BuyerProductRequest(MethodView):
    @productrequest_bp.response(200, ProductRequestSchema)
    def get(self,buyer_id):

        return [parse_requests(requests=requests) for requests in BuyerRequest.get_requests_through_buyer_id(buyer_id=buyer_id)]
      
      
def parse_requests(requests):
      return {}
    
"""
These are just some functions that make api calls i copied from the client. 
I am using them to track and revise additions.

  createproductquery,
  getqueriesthroughcategory,
  getbuyerqueries,
  getsellerqueries,
"""