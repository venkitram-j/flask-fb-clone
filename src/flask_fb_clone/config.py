"""
Configs for applcation
"""
import os


class Config:
    DEBUG = False
    TESTING = False
    
    SECRET_KEY = os.getenv("SECRET_KEY")
    
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    API_TITLE = "FB Clone REST API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    JSON_SORT_KEYS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    
    SECRET_KEY = "test-secret-key"

class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass


ENV_CONFIG_DICT = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig
)


def get_config(config_name):
    """
    Retrieve environment configuration settings.
    """
    return ENV_CONFIG_DICT.get(config_name, ProductionConfig)
