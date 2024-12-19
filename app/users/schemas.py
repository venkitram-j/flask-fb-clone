"""
Schemas for user
"""

from marshmallow import Schema, fields


class UserRegistrationSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
