from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
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

    ''' 
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'yourId@gmail.com'
    app.config['MAIL_PASSWORD'] = '*****'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    '''

    # Initialize extensions

    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Flask Login for Session based auth
    login_manager = LoginManager(app)
    login_manager.login_view = "auth.login"  # Specify the login route
    login_manager.init_app(app)

    # Initialize Flask-SocketIO with CORS
    cors.init_app(app, resources={r"/socket.io/*": {"origins": "http://127.0.0.1:5000"}})
    socketio.init_app(app, cors_allowed_origins="http://127.0.0.1:5000")  # Would be replaced with the actual domain
    # of the frontend during prod test.

    with app.app_context():
        db.create_all()

        # Import and register blueprints here
        from .routes import cart, order, payment, user, websocket, product, example, forgot_password_handler, \
            productrequest

        # Resources(endpoints) partially/completely implemented
        app.register_blueprint(user.user_blp)
        app.register_blueprint(product.product_bp)
        app.register_blueprint(forgot_password_handler.pswd_retrvl_bp)
        app.register_blueprint(cart.cart_bp)
        app.register_blueprint(order.order_bp)

        """
        app.register_blueprint(example.example_blp)
        app.register_blueprint(payment.payment_bp)
        app.register_blueprint(websocket.websocket_bp)
        """

        # Register chat test blueprints
        from .views import views
        app.register_blueprint(views)

        # Include other configurations and setup as needed

        from app.models import User

        @login_manager.user_loader
        def load_user(user_id):
            # since the user_id is just the primary key of our user table, use it in the query for the user
            return User.query.get(int(user_id))

        return app, socketio
