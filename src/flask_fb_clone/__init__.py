"""
Flask app initialization via factory pattern.
"""
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import get_config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name):
    app = Flask("flask-fb-clone")
    app.config.from_object(get_config(config_name))

    db.init_app(app)
    migrate.init_app(app, db)
    
    return app
