from flask import Flask
from flask_migrate import Migrate
from .models import Chat
from flask_socketio import SocketIO
from db import db
from flask_cors import CORS

socketio = SocketIO()
migrate = Migrate()
cors = CORS()


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(f"config.{config_name.capitalize()}Config")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    # Initialize Flask-SocketIO with CORS
    cors.init_app(app, resources={r"/socket.io/*": {"origins": "http://127.0.0.1:5000"}})
    socketio.init_app(app, cors_allowed_origins="http://127.0.0.1:5000")  # Would be replaced with the actual domain
    # of the frontend during prod test.

    with app.app_context():
        db.create_all()

        # Import and register blueprints here
        from .routes import cart, order, payment, user, websocket, example

        """app.register_blueprint(cart.cart_bp)
        app.register_blueprint(order.order_bp)
        app.register_blueprint(payment.payment_bp)
        app.register_blueprint(user.user_bp)
        app.register_blueprint(websocket.websocket_bp)"""
        app.register_blueprint(example.example_blp)

        # Include other configurations and setup as needed

        return app, socketio
