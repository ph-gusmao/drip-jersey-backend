from marshmallow import Schema, fields
from marshmallow.validate import Length, Email


class RegisterSchema(Schema):

    username = fields.String(required=True, validate=Length(min=3, max=80))

    password = fields.String(required=True, validate=Length(min=6))

    email = fields.Email(required=True)
