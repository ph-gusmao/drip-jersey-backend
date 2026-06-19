from marshmallow import Schema, fields
from marshmallow.validate import Length, Email, OneOf


class AdminUserSchema(Schema):

    role = fields.String(
        required=True,
        validate=OneOf(["ADMIN"], ["USER"], error="Role deve ser ADMIN ou USER"),
    )
