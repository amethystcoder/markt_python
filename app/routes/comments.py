from flask_smorest import Blueprint
from flask.views import MethodView
from flask import abort, request
from ..schemas import CommentSchema
from ..models.product_model import Product

comment_bp = Blueprint("products", "product", description="Endpoint for all API calls related to products", url_prefix="/products")