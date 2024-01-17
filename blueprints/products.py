import uuid
from flask.views import MethodView
from flask import request
from flask_smorest import Blueprint, abort
from db import products, shops

blueprint = Blueprint(
    "products", __name__, description="Operations on Products"
)

PRODUCT_ATTR = ["shop_id", "name", "price"]


@blueprint.route("/products/<product_id>")
class Product(MethodView):
    def get(self, product_id):
        try:
            return products[product_id]

        except KeyError:
            abort(404, message="Aborted, Product not found!.")

    def put(self, product_id):
        try:
            product_data = request.json

            if not all(key in product_data for key in PRODUCT_ATTR):
                abort(
                    400,
                    message="Aborted, Product should include price and name",
                )

            product = products[product_id]
            product |= product_data

            return product, 200

        except KeyError:
            abort(404, message="Aborted, Product not found!.")

    def delete(self, product_id):
        try:
            del products[product_id]
            return {"message", "Product Deleted"}, 200
        except KeyError:
            abort(404, message="Aborted, Product not found!.")


@blueprint.route("/products")
class ProductList(MethodView):
    def get(self):
        return {"products": list(products.values())}

    def post(self):
        new_product = request.json

        try:
            # check if keys in shop data is available
            if not all(key in new_product for key in PRODUCT_ATTR):
                abort(
                    400,
                    message=f"ONLY {','.join(PRODUCT_ATTR)} "
                    "field(s) are required",
                )

            # get the shop
            # for the product that need to place into
            shop_id = new_product["shop_id"]
            shop = shops.get(shop_id, None)

            # print("shop_id", shop_id)
            # print("shop", shop)

            if shop is None:
                return {
                    "message": (
                        f"Aborted, Shop with id={shop_id} not found!."
                        "A product must belong to a shop"
                    )
                }, 404

            shop = shops[shop_id]
            shop_products = shop["products"] or []

            # create the new product
            product_id = uuid.uuid4().hex
            product = {**new_product, "id": product_id}
            products[product_id] = product

            # update shop products
            shop_products.append(product)
            shop["products"] = shop_products

            return product

        except Exception as ex:
            abort(404, message=f"Aborted, Product or Shop not found!. {ex}")
