"""
Entrypoint for application
"""
import os
from flask import Flask

from config import config_dict


def create_app():

    app = Flask(__name__)

    app.config.from_object(config_dict[os.getenv("APP_ENV")])

    return app
