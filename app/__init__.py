from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO  # Assuming you will use Flask-SocketIO for chat
import os

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(f"config.{config_name.capitalize()}Config")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)  # Initialize Flask-SocketIO

    # Import and register blueprints here
    from .routes import cart, order, payment, user, websocket

    app.register_blueprint(cart.cart_bp)
    app.register_blueprint(order.order_bp)
    app.register_blueprint(payment.payment_bp)
    app.register_blueprint(user.user_bp)
    app.register_blueprint(websocket.websocket_bp)

    # Include other configurations and setup as needed

    return app
