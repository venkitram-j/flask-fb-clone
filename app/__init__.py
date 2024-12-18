"""
Application entrypoint
"""
import os

from flask import Flask
from flask_smorest import Api
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import config_dict


load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
api = Api()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config_dict[os.environ.get("APP_ENV")])
    
    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    
    return app
