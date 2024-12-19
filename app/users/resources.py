"""
Resources for user
"""

from http import HTTPStatus
from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app import db
from .models import UserModel
from .schemas import UserRegistrationSchema


blp = Blueprint("Users", "users", url_prefix="/users", description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    
    @blp.arguments(UserRegistrationSchema)
    def post(self, user_data):
        email = user_data.get("email")
        
        if UserModel.find_by_email(email):
            abort(HTTPStatus.CONFLICT, message=f"{email} is already registered")
        
        new_user = UserModel(**user_data)
        
        db.session.add(new_user)
        db.session.commit()
        
        response = jsonify(
            status="success",
            message="Successfully Registered!"
        )
        response.status_code = HTTPStatus.CREATED
        response.headers["Cache-Control"] = "no-store"
        response.headers["Pragma"] = "no-cache"
        return response
