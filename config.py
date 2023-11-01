import os


class BaseConfig:
    # Add your base configurations here
    API_TITLE = "Markt API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///data.db")
    MAIL_SERVER = '' #i.e smtp.gmail.com
    MAIL_PORT = 0 #i.e 8080
    MAIL_USERNAME = '' #i.e yourId@gmail.com
    MAIL_PASSWORD = ''
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    # Other configurations
    # ...


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    # Add development-specific configurations here
    # ...


class ProductionConfig(BaseConfig):
    DEBUG = False
    # Add production-specific configurations here
    # ...

# Add more configuration classes as needed
