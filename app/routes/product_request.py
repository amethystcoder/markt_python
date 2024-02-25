from flask_smorest import Blueprint
from flask.views import MethodView
from flask import abort
from app.schemas import ProductRequestSchema
from app.models.buyer_request_model import BuyerRequest
from app.models.seller_model import Seller
from app.models.buyer_model import Buyer
from app.models.user_model import User

product_request_bp = Blueprint("Product Request", "request", description="Api calls to buyer product request apis")


@product_request_bp.route("/new")
class NewProductRequest(MethodView):
    @product_request_bp.response(200, ProductRequestSchema)
    def post(self, product_request_data):
        try:
            request = BuyerRequest(product_request_data["buyer_id"], product_request_data["product_description"],
                                   product_request_data["category"])
            request.save_to_db()
        except Exception as e:
            abort(500, "could not create request")


@product_request_bp.route("/<unique_id>")
class ProductRequest(MethodView):
    @product_request_bp.response(200, ProductRequestSchema)
    def get(self, unique_id):

        return parse_requests(BuyerRequest.get_requests_through_id(unique_id))

    def delete(self, unique_id):
        try:
            request_to_delete = BuyerRequest(unique_id=unique_id)
            request_to_delete.delete_from_db()
        except Exception as e:
            abort(500, "Could not delete product request")


@product_request_bp.route("/<buyer_id>")
class BuyerProductRequest(MethodView):
    @product_request_bp.response(200, ProductRequestSchema)
    def get(self, buyer_id):
        return [parse_requests(request=request, buyer=Buyer(request.buyer_id), user_details=User(request.buyer_id)) for
                request in BuyerRequest.get_requests_through_buyer_id(buyer_id=buyer_id)]


@product_request_bp.route("/<seller_id>")
class SellerProductRequest(MethodView):
    @product_request_bp.response(200, ProductRequestSchema)
    def get(self, seller_id):
        seller = Seller(seller_id)
        seller_category = Seller.category
        return [parse_requests(request=request, buyer=Buyer(request.buyer_id), user_details=User(request.buyer_id)) for
                request in BuyerRequest.get_requests_using_category(seller_category)]


@product_request_bp.route("/category/<name>")
class ProductRequestFromCategory(MethodView):
    @product_request_bp.response(200, ProductRequestSchema)
    def get(self, name):
        return [parse_requests(request=request, buyer=Buyer(request.buyer_id), user_details=User(request.buyer_id)) for
                request in BuyerRequest.get_requests_using_category(name)]


def parse_requests(request, buyer, user_details):
    return {
        "buyer_name": buyer.username,
        "city": user_details.city,
        "state": user_details.state,
        "profile_image": user_details.profile_image,
        "query_id": request.unique_id,
        "message": request.product_description,
        "buyer_id": request.buyer_id,
        "category": request.category,
        "stale_time": request.created_at
    }
