from flask_smorest import Blueprint
from flask.views import MethodView
from flask import abort
from ..schemas import CartSchema
from ..models.cart_model import Cart
from ..models.order_model import Order
from ..models.product_model import Product
from ..models.imagename_store_model import ImageNameStore

cart_bp = Blueprint("cart", "cart", description="Endpoint for all API calls related to cart", url_prefix="/cart")

@cart_bp.route("/<buyerid>")
class BuyerCart(MethodView):
    @cart_bp.response(200, CartSchema)
    def get(buyerid):
       return [parsecart(cartitem=cartitem, image=ImageNameStore.getproductthumbnail(cartitem.product_id)) for cartitem in Cart.get_buyer_cart_items(buyer_id=buyerid)]
    
    
@cart_bp.route("/<cartid>")
class CartItem(MethodView):
  @cart_bp.response(201, CartSchema)
  def post(cartdata):
    try:
      cart = Cart(buyer_id=cartdata["buyer_id"],product_id=cartdata["product_id"],quantity=cartdata["quantity"],
                  has_discount=cartdata["has_discount"],discount_price=cartdata["discount_price"],
                  discount_percent=cartdata["discount_percent"])
      cart.save_to_db()
    except Exception as e:
      abort(500,"Could not save")
      
  @cart_bp.response(201, CartSchema)
  def put(cartid,newquantity):
    try:
      cart = Cart(cart_id=cartid)
      product = Product(product_id=cart.product_id)
      if product.stock_quantity > newquantity:
        #TODO: We need to find an appropriate status code for this response
        abort(500,"internal server error")
      else:
        cart.update_cart_quantity(newquantity=newquantity)
    except Exception as e:
      abort(500,"internal server error")
  
  @cart_bp.response(201, CartSchema)
  def delete(cartid):
    try:
      cart = Cart(cart_id=cartid)
      cart.delete_from_db()
    except Exception as e:
      abort(404,"cart item not found")
      
@cart_bp.route("/checkout/<buyer_id>")
class CheckoutCart(MethodView):
  @cart_bp.response(201, CartSchema)
  def post(cartdata):
    try:
      buyer_cart_items = Cart.get_buyer_cart_items(buyer_id=cartdata["buyer_id"])
      for cart_items in buyer_cart_items:
        product = Product(cart_items.product_id)
        if cart_items.has_discount is True and cart_items.discount_percent > 0:
          #check if this is valid in the client side
          product_total_price = cart_items.quantity * (product.price - ((cart_items.discount_percent / 100) * product.price))
        else:
          product_total_price = cart_items.quantity * product.price
        #set the delivery address using the actual address of the buyer as default
        order = Order(buyer_id=cart_items.buyer_id,product_id=product.product_id,seller_id=product.seller_id,
                      total_price=product_total_price,quantity=cart_items.quantity,delivery_address="")
        order.save_to_db()
    except Exception as e:
      abort(500,"Could not save")
        
    
def parsecart(cartitem,image):
  return {
    "buyer_id":cartitem.buyer_id,
    "product_id":cartitem.product_id,
    "quantity":cartitem.quantity,
    "has_discount":cartitem.has_discount,
    "discount_price":cartitem.discount_price,
    "discount_percent":cartitem.discount_percent,
    "product_image":image.image_name
  }       