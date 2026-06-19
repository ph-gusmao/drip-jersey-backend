from marshmallow import Schema, fields


class ProductSchema(Schema):

    name = fields.String(required=True)

    price = fields.Float(required=True)

    stock = fields.Integer(required=True)
