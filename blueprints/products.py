import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import products, shops
from schemas import ProductSchema, ProductUpdateSchema

blueprint = Blueprint(
    "products", __name__, description="Operations on Products"
)


@blueprint.route("/products")
class ProductList(MethodView):
    @blueprint.response(200, ProductSchema(many=True))
    def get(self):
        """Returns all list of products"""
        return list(products.values())

    @blueprint.arguments(ProductSchema)
    @blueprint.response(201, ProductSchema)
    def post(self, new_product):
        """Create a new product"""

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

        # check whether the product has already exists
        # in the shop's products
        if any(
            "name" in dt and dt["name"] == new_product["name"]
            for dt in shop_products
        ):
            abort(400, message="Product's name already exists in the Shop!")

        # create the new product
        product_id = uuid.uuid4().hex
        product = {**new_product, "id_": product_id}
        products[product_id] = product

        # update shop products
        shop_products.append(product)
        shop["products"] = shop_products

        return product


@blueprint.route("/products/<product_id>")
class Product(MethodView):
    @blueprint.response(200, ProductSchema)
    def get(self, product_id):
        """Returns a product data by its Id"""
        try:
            return products[product_id]

        except KeyError:
            abort(404, message="Aborted, Product not found!.")

    @blueprint.arguments(ProductUpdateSchema)
    @blueprint.response(200, ProductSchema)
    def put(self, product_data, product_id):
        """Update product by it's Id"""
        try:
            product = products[product_id]
            product |= product_data

            return product

        except KeyError:
            abort(404, message="Aborted, Product not found!.")

    def delete(self, product_id):
        """Delete a Product"""
        try:
            del products[product_id]
            return {"message": "Product Deleted"}, 200
        except KeyError:
            abort(404, message="Aborted, Product not found!.")
