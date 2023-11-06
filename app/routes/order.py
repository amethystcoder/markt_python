from flask_smorest import Blueprint
from flask.views import MethodView
from flask import abort
from app.models.order_model import Order
from app.models.user_model import User

from app.schemas import OrderSchema

order_bp = Blueprint("Orders", "orders", description="Endpoints and routes for everything related to orders")

@order_bp.route("/new")
class Order(MethodView):
    @order_bp(201, OrderSchema)
    def post(self,data):
        try:
           pass 
        except Exception as e:
            abort(500,"could not create")
            
@order_bp.route("/<seller_id>")
class PendingOrders(MethodView):
    @order_bp(201, OrderSchema)
    def get(self,data):
        try:
           pass 
        except Exception as e:
            abort(500,"could not create")
            
            
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
