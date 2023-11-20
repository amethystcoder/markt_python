from flask_smorest import Blueprint
from flask.views import MethodView
from flask import abort, request
from ..schemas import FavoriteSchema
from ..models.product_model import Product

favorite_bp = Blueprint("favorites", "favorite", description="Endpoint for all API calls related to buyer favorites", url_prefix="/favorites")