from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_cors import CORS

import app.models

from db import db
# from .chat_websocket import socketio
from flask_socketio import SocketIO

socketio = SocketIO()
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
    db.init_app(app)

    mail.init_app(app)

    migrate = Migrate(app, db)
    api = Api(app)

    # Flask Login for Session based auth
    login_manager = LoginManager(app)
    login_manager.login_view = "auth.login"  # Specify the login route
    login_manager.init_app(app)

    # Initialize Flask-SocketIO with CORS
    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    socketio.init_app(app, cors_allowed_origins="http://127.0.0.1")  # Would be replaced with the actual domain
    # of the frontend during prod test.

    with app.app_context():
        db.create_all()

        # Import and register blueprints here
        from .auth import auth_blp
        from .routes.cart import cart_bp
        from .routes.comments import comment_bp
        from .routes.favorites import favorite_bp
        from .routes.forgot_password_handler import pswd_retrvl_bp
        from .routes.order import order_bp
        # from routes.payment import payment_bp
        from .routes.product import product_bp
        from .routes.product_request import product_request_bp
        from .routes.user import user_blp

        # Resources(endpoints) partially/completely implemented
        api.register_blueprint(auth_blp)
        api.register_blueprint(user_blp)
        api.register_blueprint(product_bp)
        api.register_blueprint(pswd_retrvl_bp)
        api.register_blueprint(cart_bp)
        api.register_blueprint(order_bp)
        api.register_blueprint(favorite_bp)
        api.register_blueprint(comment_bp)
        api.register_blueprint(product_request_bp)

        """
        app.register_blueprint(example.example_blp)
        app.register_blueprint(payment.payment_bp)
        app.register_blueprint(websocket.websocket_bp)
        """

        """
        # Register chat test blueprints
        from .views import views
        app.register_blueprint(views)
        """

        # Include other configurations and setup as needed

        from app.models import User

        @login_manager.user_loader
        def load_user(user_id):
            # since the user_id is just the primary key of our user table, use it in the query for the user
            return User.query.get(int(user_id))

        return app, socketio
