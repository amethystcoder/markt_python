import os


class BaseConfig:
    # Add your base configurations here
    API_TITLE = "Markt API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///data.db")
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
