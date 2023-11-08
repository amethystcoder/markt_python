from flask_smorest import Blueprint
from flask.views import MethodView
from flask import abort
from app.models.order_model import Order
from app.models.user_model import User
from app.models.seller_model import Seller
from app.models.buyer_model import Buyer
from app.models.product_model import Product

from app.models.imagename_store_model import ImageNameStore

from app.schemas import OrderSchema

order_bp = Blueprint("Orders", "orders", description="Endpoints and routes for everything related to orders")

@order_bp.route("/new")
class Order(MethodView):
  @order_bp.response(201, OrderSchema)
  def post(self,data):
    try:
      order = Order(buyer_id = data["buyer_id"],seller_id = data["seller_id"],product_id = data["product_id"],
                    quantity = data["quantity"],total_price = data["total_price"],
                    delivery_address = data["delivery_address"])
      order.save_to_db()
    except Exception as e:
        abort(500,"could not create")
            
@order_bp.route("/sellers/pending/<seller_id>")
class PendingOrders(MethodView):
  @order_bp.response(200, OrderSchema)
  def get(self,seller_id):
    try:
        return [parse_unaccepted_orders(order=order,buyer=Buyer(order.buyer_id),product=Product(order.product_id),product_image=ImageNameStore.getproductthumbnail(order.product_id)) for order in Order.get_seller_pending_orders(seller_id)]
    except Exception as e:
        abort(500,"could not create")
            
@order_bp.route("/sellers/accepted/<seller_id>")
class AcceptedOrders(MethodView):
  @order_bp.response(200, OrderSchema)
  def get(self,seller_id):
    try:
        [parse_unaccepted_orders(order=order,buyer=Buyer(order.buyer_id),product=Product(order.product_id),product_image=ImageNameStore.getproductthumbnail(order.product_id)) for order in Order.get_seller_accepted_orders(seller_id)]
    except Exception as e:
      abort(500,"could not create")
      
@order_bp.route("/sellers/update/accept")
class AcceptOrders():
  @order_bp.response(200, OrderSchema)
  #authentication would be needed
  def patch(self,order_id):
    try:
      order = Order(order_id=order_id)
      order.accept_order()
    except Exception as e:
      abort(404,"order not found")

@order_bp.route("/sellers/update/decline")
class DeclineOrders():
  @order_bp.response(200, OrderSchema)
  #authentication would be needed
  def patch(self,order_id):
    try:
      order = Order(order_id=order_id)
      order.decline_order()
    except Exception as e:
      abort(404,"order not found")

@order_bp.route("/buyers/<buyer_id>")
class BuyerOrders():
  @order_bp.response(200, OrderSchema)
  def get(self,buyer_id):
    try:
        [parse_buyer_orders(order=order,buyer=Buyer(order.buyer_id),product=Product(order.product_id),seller=Seller(order.seller_id),product_image=ImageNameStore.getproductthumbnail(order.product_id)) for order in Order.get_buyer_orders(buyer_id)]
    except Exception as e:
      abort(500,"could not create")
      
''' @order_bp.route("/buyers/update/complete")
class CompleteOrders():
  @order_bp.response(200, OrderSchema)
  def patch(self,order_id):
    try:
      order = Order(order_id=order_id)
      order.complete_order()
    except Exception as e:
      abort(404,"order not found") '''
            
def parse_unaccepted_orders(order,buyer,product,product_image):
    return {
        "order_id":order.order_id,
        "seller_id":order.seller_id,
        "product_quantity":order.quantity,
        "order_date":order.order_date,
        "product_name":product.name,
        "total_price":order.total_price,
        "product_id":order.product_id,
        "product_image":product_image,
        "buyer_id":order.buyer_id,
        "buyer_name":buyer.username
        }

def parse_orders(order,seller,buyer,product,product_image):
    return {
        "order_id":order.order_id,
        "seller_id":order.seller_id,
        "product_quantity":order.quantity,
        "order_date":order.order_date,
        "product_name":product.name,
        "total_price":order.total_price,
        "product_id":order.product_id,
        "product_image":product_image,
        "buyer_id":order.buyer_id,
        "buyer_name":buyer.username
        }

def parse_buyer_orders(order: Order,seller,buyer,product,product_image):
    return {
      "order_id":order.order_id,
        "seller_id":order.seller_id,
        "product_quantity":order.quantity,
        "order_date":order.order_date,
        "product_name":product.name,
        "total_price":order.total_price,
        "product_id":order.product_id,
        "product_image":product_image,
        "buyer_id":order.buyer_id,
        "buyer_name":buyer.username,
        "seller_shopname":seller.shop_name,
        "order_status":order.order_status,
        "delivery_name":"",
        "delivery_id":"",
        "received_by_delivery":False
        }

def parse_successful_orders(order,seller,buyer,product,product_image):
    return {
      "seller_id":order.seller_id,
      "product_name":product.name,
      "total_price":order.total_price,
      "product_quantity":order.quantity
        }
"""
This is a list of functions i took from the client side that interact with the order backend from the
php backend. I am just adding them here so i can be reminded of the endpoints i want to add.

getpendingorders(sellerid:string){
    return this.http.get<Array<UnacceptedOrders>>(
      `http://localhost/markt_php/get_non_accepted_orders.php?user_type=seller&user_id=${sellerid}`
      )
    .pipe(
      retry(2)
    )
  }

  getacceptedorders(sellerid:string){
    return this.http.get<Array<Orders>>(
      `http://localhost/markt_php/get_accepted_orders.php?user_type=seller&user_id=${sellerid}`
      )
    .pipe(
      retry(2)
    )
  }

  acceptorder(orderid:string,user_id:string,user_type:string){
    let formdata = new FormData()
    formdata.append('order_id',orderid)
    formdata.append('user_id',user_id)
    formdata.append('user_type',user_type)
    return this.http.post(
      "http://localhost/markt_php/accept_order.php",
      formdata
    ).pipe(
      retry(2)
    )
  }

  declineorder(orderid:string,user_id:string,user_type:string){
    let formdata = new FormData()
    formdata.append('order_id',orderid)
    formdata.append('user_id',user_id)
    formdata.append('user_type',user_type)
    return this.http.post<boolean>(
      "http://localhost/markt_php/decline_order.php",
      formdata
    ).pipe(
      retry(2)
    )
  }

  getbuyerorders(buyer_id:string){
    return this.http.get<BuyerOrders[]>(
      `http://localhost/markt_php/get_buyer_orders.php?user_type=buyer&user_id=${buyer_id}`
      )
    .pipe(
      retry(2)
    )
  }

  getclosedeliveryorders(deliveryid:string,longtitude:number|undefined = undefined,latitude:number|undefined = undefined){
    if(longtitude && latitude)
    return this.http.get<DeliveryOrders[]>(
      `http://localhost/markt_php/get_delivery_orders.php?
        user_type=delivery&user_id=${deliveryid}
        &longtitude=${longtitude}&latitude=${latitude}`
      )
    .pipe(
      retry(2)
    )

    return this.http.get<DeliveryOrders[]>(
      `http://localhost/markt_php/get_delivery_orders.php?user_type=delivery&user_id=${deliveryid}`
      )
    .pipe(
      retry(2)
    )
  }

  private handleerror(err:HttpErrorResponse){
    if(err.status == 0){}
    else{}
    return throwError(()=>{ new Error("something unexpected happened") })
  }

  createorders(user_id:string,user_type:string){
    let neworderdata = new FormData()
    neworderdata.append("user_id",user_id)
    neworderdata.append("user_type",user_type)
    return this.http.post<SuccessfulOrder[]>(
      "http://localhost/markt_php/create_new_orders.php",
      neworderdata
    ).pipe(
      retry(2)
    )
  }
"""
