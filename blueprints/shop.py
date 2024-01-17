import uuid
from flask.views import MethodView
from flask import request
from flask_smorest import Blueprint, abort
from db import shops

blueprint = Blueprint("shops", __name__, description="Operations on Shops")

SHOP_ATTR = ["name", "address"]


@blueprint.route("/shops/<shop_id>")
class Shop(MethodView):
    def get(self, shop_id):
        try:
            return shops[shop_id]

        except KeyError:
            abort(404, message="Aborted, Shop not found!")

    def delete(self, shop_id):
        try:
            del shops[shop_id]
            return {"message", "Shop Deleted"}, 200
        except KeyError:
            abort(404, message="Aborted, Shop not found!")


@blueprint.route("/shops")
class ShopList(MethodView):
    def get(self):
        return {"shops": list(shops.values())}

    def post(self):
        shop_data = request.json

        # check if keys in shop data is available
        if not all(key in shop_data for key in SHOP_ATTR):
            abort(
                400,
                message=f"ONLY {','.join(SHOP_ATTR)} field(s) are required!",
            )

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
        shop = {**shop_data, "id": shop_id, "products": []}

        shops[shop_id] = shop

        return shop, 201
