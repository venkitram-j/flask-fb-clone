"""
Configs for application
"""

class BaseConfig:
    DEBUG = False

class DevConfig(BaseConfig):
    DEBUG = True
    
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    API_TITLE = "FB Clone REST API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

class ProdConfig(BaseConfig):
    pass


config_dict = {
    "dev": DevConfig,
    "prod": ProdConfig
}
