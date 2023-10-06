from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from .image_resizer_and_uploader import ImageSaver
from ..schemas import ProductSchema,CategorySchema
from ..models.product_model import Product
from ..models.categories_get import Categories
from ..models.imagename_store_model import ImageNameStore

product_bp = Blueprint("products", "product", description="Endpoint for all API calls related to products", url_prefix="/products")

@product_bp.route("/new")
class Products(MethodView):
    @product_bp.response(200, ProductSchema)
    def post(self,product_data):
      """
      
        Creates a new product
      Args:
          product_data (_dict_): a dictionary containing information about the product
      Returns:
          _dict_ | bool: the product
      """
      try:
        product = Product(product_data["seller_id"],product_data["product_name"],
                        product_data["description"],product_data["product_price"],
                        product_data["quantity"],product_data["category"])
        product_images = request.files
        
        #Product images would be added to uploads folder and database
        
        product.save_to_db()
        return parsedict(product=product)
      except ConnectionError:
        return False

@product_bp.route("/<product_id>")
class Products(MethodView):
    @product_bp.response(200, ProductSchema)
    def get(self,product_id):
          
      """
      gets a particular product using its id, along with its images
      seller description, e.t.c
      """
      product = Product.get_product_using_id(product_id)
      
      return parsedict(product=product,images=ImageNameStore.getproductimages(product_id=product_id))
    
    #edit product
    @product_bp.response(200, ProductSchema)
    def patch(self,product_data):
          
      return 
    
    @product_bp.response(200, ProductSchema)
    def delete(self,product_id):
      product_to_delete = Product(product_id=product_id)
      return product_to_delete.delete_from_db()
      
@product_bp.route("/categories/<type>")
class Categories(MethodView):
    @product_bp.response(200, CategorySchema)
    def get(self,type):
      """
      gets a particular product using its id, along with its images
      seller description, e.t.c
      """
      category_tags = Categories()
      match type:
        case "tags":
          return category_tags.get_all_tags()
        case "categorynames":
          return category_tags.get_category_names()
        case "all":
          return category_tags.get_all_categories_and_tags()
        case _:
          return category_tags.get_all_categories_and_tags()


@product_bp.route("/random/<amount>")
class RandomProducts(MethodView):
    @product_bp.response(200, ProductSchema)
    def get(self, amount):
          
      return [parsedict(product=product,images=[ImageNameStore.getproductthumbnail(product.product_id)]) for product in Product.get_random_products(amount)]
      
@product_bp.route("/seller/<seller_id>")
class SellerProducts(MethodView):
    @product_bp.response(200, ProductSchema)
    def get(self,seller_id):
      
      return [parsedict(product=product,images=ImageNameStore.getproductthumbnail(product.product_id)) for product in Product.get_products_using_sellerid(seller_id)]

@product_bp.route("/search/<name>")
class ProductSearch(MethodView):
    @product_bp.response(200, ProductSchema)
    def get(self,name):
      
      return [parsedict(product=product,images=ImageNameStore.getproductthumbnail(product.product_id)) for product in Product.search_product_using_name(name)]

@product_bp.route("/category/search/<name>")
class ProductSearch(MethodView):
    @product_bp.response(200, ProductSchema)
    def get(self,category_name):
      
      return [parsedict(product=product,images=ImageNameStore.getproductthumbnail(product.product_id)) for product in Product.search_product_using_category(category_name)]      
      
def parsedict(product,images):
  return {
    "seller_id":product.seller_id,
    "product_name":product.name,
    "description":product.description,
    "product_price":product.price,
    "quantity":product.stock_quantity,
    "category":product.category,
    "product_id":product.product_id,
    "product_images":[image for image in images]
    }
  
#TODO: searchproductwithcategory