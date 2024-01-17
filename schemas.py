from marshmallow import Schema, fields


class ProductSchema(Schema):
    id_ = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    shop_id = fields.Str(required=True)


class ProductUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    shop_id = fields.Str(required=True)


class ShopSchema(Schema):
    id_ = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    address = fields.Str(required=True)
