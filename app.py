from flask import Flask, request

app = Flask(__name__)


shops = [
    {"name": "clicky88", "products": [{"name": "laptop", "price": 800}]},
    {"name": "abu90", "products": [{"name": "calculator", "price": 25}]},
]


@app.route("/shops")
def hello():
    return shops


@app.route("/shops", methods=["POST"])
def create_shop():
    shop = request.json

    shops.append(shop)

    return shop, 201


if __name__ == "__main__":
    app.run()
