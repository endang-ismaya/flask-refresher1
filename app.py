import uuid
from flask import Flask, request
from db import shops, products

app = Flask(__name__)

SHOP_ATTR = ["name", "address"]
PRODUCT_ATTR = ["shop_id", "name", "price"]


@app.route("/shops")
def get_shops():
    return {"shops": list(shops.values())}


@app.route("/shops/<shop_id>", methods=["get"])
def get_shop(shop_id):
    try:
        return shops[shop_id]

    except KeyError:
        return {"message": "Shop not found"}, 404


@app.route("/shops", methods=["post"])
def create_shop():
    shop_data = request.json

    # check if keys in shop data is available
    if not all(key in shop_data for key in SHOP_ATTR):
        return (
            {"message": f"ONLY {','.join(SHOP_ATTR)} field(s) are required"},
            400,
        )

    shop_id = uuid.uuid4().hex
    shop = {**shop_data, "id": shop_id, "products": []}

    shops[shop_id] = shop

    return shop, 201


@app.route("/shops/<shop_id>", methods=["delete"])
def delete_shop(shop_id):
    try:
        del shops[shop_id]
        return {"message", "Shop Deleted"}, 200
    except KeyError:
        return {"message": "Shop not found"}, 404


@app.route("/products", methods=["post"])
def create_product():
    new_product = request.json

    try:
        # check if keys in shop data is available
        if not all(key in new_product for key in PRODUCT_ATTR):
            return (
                {
                    "message": f"ONLY {','.join(PRODUCT_ATTR)} "
                    "field(s) are required"
                },
                400,
            )

        # get the shop
        # for the product that need to place into
        shop = shops[new_product["shop_id"]]
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
        return {"message": "Shop not found", "errors": ex}, 404


@app.route("/products", methods=["get"])
def get_products():
    return {"products": list(products.values())}


@app.route("/products/<product_id>", methods=["get"])
def get_product(product_id):
    try:
        return products[product_id]

    except KeyError:
        return {"message": "Product not found"}, 404


@app.route("/products/<product_id>", methods=["delete"])
def delete_product(product_id):
    try:
        del products[product_id]
        return {"message", "Product Deleted"}, 200
    except KeyError:
        return {"message": "Product not found"}, 404


@app.route("/products/<product_id>", methods=["put"])
def update_product(product_id):
    try:
        product_data = request.json

        if not all("price" in product_data, "name" in product_data):
            return {"message": "Product should include price and name"}, 400

        product = products[product_id]
        product |= product_data

        return product, 200

    except KeyError:
        return {"message": "Product not found"}, 404


if __name__ == "__main__":
    app.run()
