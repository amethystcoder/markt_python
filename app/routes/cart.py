from flask_smorest import Blueprint
from flask.views import MethodView
from ..schemas import CartSchema

cart_bp = Blueprint("cart", "cart", description="Endpoint for all API calls related to cart", url_prefix="/cart")

@cart_bp.route("/<buyerid>")
class Cart(MethodView):
    @cart_bp.response(200, CartSchema)
    def get(buyerid):
      pass
    
    def post(buyerid):
      pass
    
    def delete(buyerid):
      pass
"""
  getbuyerbasketitems,
  additemtocart,
  removeitemfromcart,
"""        