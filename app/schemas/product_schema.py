from marshmallow import Schema, fields, validate
from marshmallow.validate import Length, Range


class ProductSchema(Schema):

    id = fields.Int(dump_only=True)

    name = fields.Str(required=True, validate=validate.length(min=3, max=100))

    price = fields.Float(required=True, validate=validate.Range(min=0.01))

    stock = fields.Integer(required=True, validate=validate.Range(min=0))


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
