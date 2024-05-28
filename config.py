"""
Configs for application
"""
import os

from dotenv import load_dotenv
load_dotenv()


class BaseConfig:

    DEBUG = False
    TESTING = False

    SECRET_KEY = os.getenv("SECRET_KEY")


class DevelopmentConfig(BaseConfig):

    DEBUG = True


class TestingConfig(BaseConfig):

    DEBUG = True
    TESTING = True

    SECRET_KEY = "test-secret"


class ProductionConfig(BaseConfig):

    pass


config_dict = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "prod": ProductionConfig
}
