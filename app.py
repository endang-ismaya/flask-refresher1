from flask import Flask
from flask_smorest import Api

# apps
from blueprints.shop import blueprint as ShopBP
from blueprints.products import blueprint as ProductBP

app = Flask(__name__)

SHOP_ATTR = ["name", "address"]
PRODUCT_ATTR = ["shop_id", "name", "price"]

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Shops REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config[
    "OPENAPI_SWAGGER_UI_URL"
] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"


api = Api(app=app)
api.register_blueprint(ShopBP)
api.register_blueprint(ProductBP)


if __name__ == "__main__":
    app.run()
