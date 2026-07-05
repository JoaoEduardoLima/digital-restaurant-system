from flask import Flask
from app.routes.menu import menu_bp
from app.routes.order import order_bp
from app.routes.cart import cart_bp
from app.services.utils import usd, translate_status_customer, translate_status_restaurant
from app.routes.clear_cart import clear_cart_bp
from app.routes.remove_item import remove_item_bp
from app.routes.login import login_bp, logout
from app.routes.kitchen import kitchen_bp
from app.routes.checkout import checkout_bp
from app.routes.stream import kitchen_stream_bp

def create_app():
    app = Flask(__name__)
    # for custommer
    app.secret_key = "1971e235c687fa2fc7fa5b03ab80a2186b7b81c9e89845915cac6539b12e29e5"
    app.register_blueprint(menu_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(clear_cart_bp)
    app.register_blueprint(remove_item_bp)

    # for restaurant
    app.register_blueprint(login_bp)
    app.register_blueprint(kitchen_bp)
    app.register_blueprint(checkout_bp)
    app.register_blueprint(kitchen_stream_bp)

    # Makes the feature available for templates.
    app.jinja_env.filters["usd"] = usd
    app.jinja_env.filters["translate_status_customer"] = translate_status_customer
    app.jinja_env.filters["translate_status_restaurant"] = translate_status_restaurant
    return app
