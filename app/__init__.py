from flask import Flask
from flask_migrate import Migrate
import os
from .chat_websocket import socketio
from db import db

migrate = Migrate()


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(f"config.{config_name.capitalize()}Config")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)  # Initialize Flask-SocketIO

    # Import and register blueprints here
    from .routes import cart, order, payment, user, websocket, product, productquery, example

    app.register_blueprint(cart.cart_bp)
    app.register_blueprint(order.order_bp)
    app.register_blueprint(payment.payment_bp)
    app.register_blueprint(payment.productquery_bp)
    app.register_blueprint(user.user_bp)
    app.register_blueprint(websocket.websocket_bp)
    app.register_blueprint(product.product_bp)
    app.register_blueprint(example.example_blp)

    # Include other configurations and setup as needed

    return app
