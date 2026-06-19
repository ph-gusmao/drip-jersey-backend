from marshmallow import Schema, fields
from marshmallow.validate import Length, Range


class ProductSchema(Schema):

    name = fields.String(required=True, validate=Length(min=3, max=100))

    price = fields.Float(required=True, validate=Range(min=0.01))

    stock = fields.Integer(required=True, validate=Range(min=0))
