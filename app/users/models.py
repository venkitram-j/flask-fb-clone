"""
User model.
"""
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class UserModel(db.Model):

    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return (
            f"<User email={self.email}>"
        )
    
    @property
    def password(self):
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
