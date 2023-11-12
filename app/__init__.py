from flask import Flask
from flask_migrate import Migrate
import app.models
from db import db
from flask_mail import Mail
from flask_cors import CORS

from .chat_websocket import socketio
migrate = Migrate()
cors = CORS()
mail = Mail()


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(f"config.{config_name.capitalize()}Config")

    ''' app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'yourId@gmail.com'
    app.config['MAIL_PASSWORD'] = '*****'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True '''

    # Initialize extensions
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    # Initialize Flask-SocketIO with CORS
    cors.init_app(app, resources={r"/socket.io/*": {"origins": "http://127.0.0.1:5000"}})
    socketio.init_app(app, cors_allowed_origins="http://127.0.0.1:5000")  # Would be replaced with the actual domain
    # of the frontend during prod test.

    with app.app_context():
        db.create_all()

        # Import and register blueprints here
        from .routes import cart, order, payment, user, websocket, product, example, forgot_password_handler, productrequest

        app.register_blueprint(cart.cart_bp)
        app.register_blueprint(order.order_bp)
        app.register_blueprint(payment.payment_bp)
        app.register_blueprint(user.user_bp)
        app.register_blueprint(websocket.websocket_bp)
        app.register_blueprint(product.product_bp)
        app.register_blueprint(example.example_blp)
        app.register_blueprint(forgot_password_handler.pswd_retrvl_bp)

        # Register chat test blueprints
        from .views import views
        app.register_blueprint(views)

        # Include other configurations and setup as needed

        return app, socketio
