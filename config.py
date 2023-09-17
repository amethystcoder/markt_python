import os


class BaseConfig:
    # Add your base configurations here
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
