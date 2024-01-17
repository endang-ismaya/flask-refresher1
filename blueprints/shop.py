import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import shops
from schemas import ShopSchema

blueprint = Blueprint("shops", __name__, description="Operations on Shops")


@blueprint.route("/shops")
class ShopList(MethodView):
    @blueprint.response(200, ShopSchema(many=True))
    def get(self):
        """Returns the list of shops"""
        return list(shops.values())

    @blueprint.arguments(ShopSchema)
    @blueprint.response(201, ShopSchema)
    def post(self, shop_data):
        """Creating a new Shop"""
        if any(
            shop_item
            for shop_item in shops.values()
            if shop_data["name"] == shop_item["name"]
        ):
            abort(
                404,
                message=f'{shop_data["name"]} already exists',
            )

        shop_id = uuid.uuid4().hex
        shop = {**shop_data, "id_": shop_id, "products": []}

        shops[shop_id] = shop

        return shop


@blueprint.route("/shops/<shop_id>")
class Shop(MethodView):
    @blueprint.response(200, ShopSchema)
    def get(self, shop_id):
        """Returns a shop by giving it's id"""
        try:
            return shops[shop_id]

        except KeyError:
            abort(404, message="Aborted, Shop not found!")

    def delete(self, shop_id):
        """Delete a Shop"""
        try:
            del shops[shop_id]
            return {"message": "Shop Deleted"}, 200
        except KeyError:
            abort(404, message="Aborted, Shop not found!")
