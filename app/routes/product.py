from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import request

from ..schemas import ProductSchema, CategorySchema
from ..models.categories_get import get_all_categories_and_tags, get_all_tags, get_category_names

from ..models import Product, ImageNameStore
from ..utils import parse_dict, ImageSaver
import tempfile

product_bp = Blueprint("products", "product", description="Endpoint for all API calls related to products",
                       url_prefix="/products")


@product_bp.route("/new")
class Products(MethodView):
    @product_bp.arguments(ProductSchema)
    @product_bp.response(201, ProductSchema)
    def post(self, product_data):
        """
      Creates a new product
      Args: product_data (_dict_): a dictionary containing information about the product
      Returns:_dict_ | bool: the product
      """
        try:
            product = Product(product_data["seller_id"], product_data["product_name"],
                              product_data["description"], product_data["product_price"],
                              product_data["quantity"], product_data["category"])
            product.setproductid()
            product_images = request.files
            for key, file in product_images.items():
                # Product images would be added to uploads folder and database
                if ImageSaver.is_valid_file(file.filename) and ImageSaver.is_valid_file_size(
                        file.content_length) and ImageSaver.is_valid_mime(file.mimetype):
                    # compress image and remove image background
                    # would add an optional parameter incase a seller does not want his image removed
                    location = tempfile.gettempdir() + '/' + file.filename
                    saved_image_name = ImageSaver.compress_image_and_remove_background(location)
                    if saved_image_name is not False and type(saved_image_name) == str:
                        new_image = ImageNameStore(saved_image_name, 'products', product.product_id)
                        new_image.save_to_db()
            product.save_to_db()
            return parse_dict(product=product, images=[])
        except Exception as e:
            abort(500, message="Could not save Successfully")


@product_bp.route("/<product_id>")
class Products(MethodView):
    @product_bp.response(200, ProductSchema)
    def get(self, product_id):
        """
      gets a particular product using its id, along with its images
      seller description, e.t.c
      """
        product = Product.get_product_using_id(product_id)

        return parse_dict(product=product, images=ImageNameStore.getproductimages(product_id=product_id))

    # edit product
    @product_bp.response(201, ProductSchema)
    def put(self, product_id, product_data):
        """
      product_data is a dictionary containing the product data to update
      """
        try:
            product = Product(product_id=product_id)
            return product.update_product(product_data)
        except Exception as e:
            abort(404, message="Item not found.")

    @product_bp.response(200, ProductSchema)
    def delete(self, product_id):
        try:
            product_to_delete = Product(product_id=product_id)
            product_to_delete.delete_from_db()
            return True
        except Exception as e:
            abort(404, message="Item not found.")


@product_bp.route("/categories/<type>")
class Categories(MethodView):
    @product_bp.response(200, CategorySchema)
    def get(self, type):
        """
      gets a 
      """
        match type:
            case "tags":
                return get_all_tags()
            case "categorynames":
                return get_category_names()
            case "all":
                return get_all_categories_and_tags()
            case _:
                return get_all_categories_and_tags()


@product_bp.route("/random/<amount>")
class RandomProducts(MethodView):
    @product_bp.response(200, ProductSchema)
    def get(self, amount):
        return [parse_dict(product=product, images=[ImageNameStore.getproductthumbnail(product.product_id)]) for product
                in Product.get_random_products(amount)]


@product_bp.route("/seller/<seller_id>")
class SellerProducts(MethodView):
    @product_bp.response(200, ProductSchema)
    def get(self, seller_id):
        return [parse_dict(product=product, images=ImageNameStore.getproductthumbnail(product.product_id)) for product in
                Product.get_products_using_sellerid(seller_id)]


@product_bp.route("/search/<name>")
class ProductSearch(MethodView):
    @product_bp.response(200, ProductSchema)
    def get(self, name):
        return [parse_dict(product=product, images=ImageNameStore.getproductthumbnail(product.product_id)) for product in
                Product.search_product_using_name(name)]


@product_bp.route("/category/search/<name>")
class ProductSearch(MethodView):
    @product_bp.response(200, ProductSchema)
    def get(self, category_name):
        return [parse_dict(product=product, images=ImageNameStore.getproductthumbnail(product.product_id)) for product in
                Product.search_product_using_category(category_name)]


# TODO: searchproductwithcategory
