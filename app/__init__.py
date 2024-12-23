"""
Flask app initialization via factory pattern.
"""
import os

from flask import Flask, jsonify
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
    
    # load user
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_headers, jwt_data):
        identity = jwt_data["sub"]
        from app.users.models import UserModel
        return UserModel.query.filter_by(id=identity).one_or_none()

    # additional claims

    @jwt.additional_claims_loader
    def make_additional_claims(identity):
        if identity == "janedoe123":
            return {"is_staff": True}
        return {"is_staff": False}

    # jwt error handlers

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({"message": "Token has expired", "error": "token_expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "message": "Request doesnt contain valid token",
                    "error": "authorization_header",
                }
            ),
            401,
        )
    
    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(jwt_header,jwt_data):
        jti = jwt_data['jti']
        from app.users.models import TokenBlocklist
        token = db.session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).scalar()
        return token is not None
    
    return app
