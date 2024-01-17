from flask import Flask, request

app = Flask(__name__)


shops = [
    {"name": "clicky88", "products": [{"name": "laptop", "price": 800}]},
    {"name": "abu90", "products": [{"name": "calculator", "price": 25}]},
]


@app.route("/shops")
def hello():
    return shops


@app.route("/shops", methods=["post"])
def create_shop():
    shop = request.json

    shops.append(shop)

    return shop, 201


@app.route("/shops/<shop_name>/product", methods=["post"])
def create_product(shop_name):
    product = request.json

    for shop in shops:
        if shop["name"] == shop_name:
            shop["products"].append(product)
            return product, 201

    return {"message": "Shop not found"}, 404


@app.route("/shops/<shop_name>", methods=["get"])
def get_shop_by_name(shop_name):
    shop = [item for item in shops if item["name"] == shop_name]

    if shop:
        return shop[0], 200

    return {"message": "Shop not found"}, 404


if __name__ == "__main__":
    app.run()
