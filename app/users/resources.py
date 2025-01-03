"""
Resources for user
"""
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import get_jwt, jwt_required, create_access_token

from app import db
from .models import UserModel, TokenBlocklist
from .schemas import UserSchema, UserLoginSchema


blp = Blueprint("Users", "users", description="Operations on users")


@blp.route("/register")
class UserRegisterView(MethodView):
    
    @blp.arguments(UserSchema)
    def post(self, user_data):
        email = user_data.get("email")
        
        if UserModel.find_by_email(email):
            abort(409, message=f"Provided email is already registered!")
        
        new_user = UserModel(**user_data)
        
        db.session.add(new_user)
        db.session.commit()
        
        return {"message": "Registered Successfully!"}, 201

@blp.route("/login")
class UserLoginView(MethodView):
    
    @blp.arguments(UserLoginSchema)
    def post(self, user_data):
        user = UserModel.find_by_email(user_data["email"])

        if user and user.check_password(user_data["password"]):
            access_token = create_access_token(identity=str(user.id))
            return {"access_token": access_token}, 200

        abort(401, message="Invalid credentials.")

@blp.route("/")
class UserListView(MethodView):
    
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()

@blp.route("/<uuid:user_id>")
class UserView(MethodView):
    
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(str(user_id))
        return user
    
    @blp.doc(security=[{"bearerAuth": []}])
    def delete(self, user_id):
        user = UserModel.query.get_or_404(str(user_id))
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted!"}, 200

@blp.route("/logout")
class UserLogoutView(MethodView):
    
    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    def post(self):
        jwt = get_jwt()
        jti = jwt['jti']
        
        token_b = TokenBlocklist(jti=jti)
        
        db.session.add(token_b)
        db.session.commit()
        
        return {"message": f"Logged out successfully!"} , 200
