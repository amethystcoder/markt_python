from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from ..schemas import ProductSchema
product_bp = Blueprint("products", "product", description="Endpoint for all API calls related to products", url_prefix="/products")

@product_bp.route("/<product-id>")
class Products(MethodView):
    @product_bp.response(200, ProductSchema)
    def get(self):
      """
      gets a particular product using its id, along with its images
      seller description, e.t.c
      """
      return {"message": "This is an example endpoint response"}
    
    @product_bp.response(200, ProductSchema)
    def delete(self):
      
        return {"message": "This is an example endpoint response"}


@product_bp.route("/random")
class RandomProducts(MethodView):
    @product_bp.response(200, ProductSchema)
    def get(self):
      
        return {"message": "This is an example endpoint response"}


"""
getcategorynames,
getcategories,
  getsellerproducts,
  searchproduct,
  searchcategory,
  searchproductwithcategory,
  getproduct,
  createproduct,
  editproduct,
  getbuyerbasketitems,
  additemtocart,
  removeitemfromcart,
  createproductquery,
  getqueriesthroughcategory,
  getbuyerqueries,
  getsellerqueries,
  deleteproduct
"""       