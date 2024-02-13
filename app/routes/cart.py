from flask_smorest import Blueprint
from flask.views import MethodView
from flask import abort
from ..schemas import CartSchema
from ..models.cart_model import Cart
from ..models.order_model import Order
from ..models.product_model import Product
from ..models.imagename_store_model import ImageNameStore

cart_bp = Blueprint("cart", "cart", description="Endpoint for all API calls related to cart", url_prefix="/cart")


@cart_bp.route("/<buyer_id>")
class BuyerCart(MethodView):
    @cart_bp.response(200, CartSchema)
    def get(self, buyer_id):
        return [parse_cart(cart_item=cart_item, image=ImageNameStore.getproductthumbnail(cart_item.product_id)) for cart_item
                in Cart.get_buyer_cart_items(buyer_id=buyer_id)]


@cart_bp.route("/<cart_id>")
class CartItem(MethodView):
    @cart_bp.response(201, CartSchema)
    def post(self, cart_data):  # /cart_id shouldn't be used to create a cart, id is yet tbc
        try:
            cart = Cart(buyer_id=cart_data["buyer_id"], product_id=cart_data["product_id"], quantity=cart_data["quantity"],
                        has_discount=cart_data["has_discount"], discount_price=cart_data["discount_price"],
                        discount_percent=cart_data["discount_percent"])
            cart.save_to_db()
        except Exception as e:
            abort(500, "Could not save")

    @cart_bp.response(201, CartSchema)
    def put(self, cart_id, new_quantity):
        try:
            cart = Cart(cart_id=cart_id)
            product = Product(product_id=cart.product_id)
            if product.stock_quantity > new_quantity:
                # TODO: We need to find an appropriate status code for this response
                abort(500, "internal server error")
            else:
                cart.update_cart_quantity(new_quantity)
        except Exception as e:
            abort(500, "internal server error")

    @cart_bp.response(201, CartSchema)
    def delete(self, cart_id):
        try:
            cart = Cart(cart_id=cart_id)
            cart.delete_from_db()
        except Exception as e:
            abort(404, "cart item not found")


@cart_bp.route("/checkout/<buyer_id>")
class CheckoutCart(MethodView):
    @cart_bp.response(201, CartSchema)
    def post(self, cart_data):
        try:
            buyer_cart_items = Cart.get_buyer_cart_items(buyer_id=cart_data["buyer_id"])
            for cart_items in buyer_cart_items:
                product = Product(cart_items.product_id)
                if cart_items.has_discount is True and cart_items.discount_percent > 0:
                    # check if this is valid in the client side
                    product_total_price = cart_items.quantity * (
                                product.price - ((cart_items.discount_percent / 100) * product.price))
                else:
                    product_total_price = cart_items.quantity * product.price
                # set the delivery address using the actual address of the buyer as default
                order = Order(buyer_id=cart_items.buyer_id, product_id=product.product_id, seller_id=product.seller_id,
                              total_price=product_total_price, quantity=cart_items.quantity, delivery_address="")
                order.save_to_db()
                Cart.delete_all_buyer_cart_items(buyer_id=cart_data["buyer_id"])
        except Exception as e:
            abort(500, "Could not save")


def parse_cart(cart_item, image):
    return {
        "buyer_id": cart_item.buyer_id,
        "product_id": cart_item.product_id,
        "quantity": cart_item.quantity,
        "has_discount": cart_item.has_discount,
        "discount_price": cart_item.discount_price,
        "discount_percent": cart_item.discount_percent,
        "product_image": image.image_name
    }
