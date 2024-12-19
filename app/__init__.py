"""
Flask app initialization via factory pattern.
"""
import os

from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from config import get_config

db = SQLAlchemy()
migrate = Migrate()
api = Api()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(get_config(os.getenv("APP_ENV", "testing")))
    app.json.sort_keys = False

    from app.users.models import UserModel
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    api.init_app(app)
    
    api_root = app.config["API_ROOT"]
    from app.users.resources import blp as user_blp
    api.register_blueprint(user_blp, url_prefix=f"{api_root}/users")
    
    return app
