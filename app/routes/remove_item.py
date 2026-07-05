import json

from flask import Blueprint, jsonify, request, make_response
from app.services.utils import MAX_AGE_COOKIE

remove_item_bp = Blueprint('remove_item', __name__)

@remove_item_bp.route('/remove_item', methods=['POST'])
def remove_item():
    data = request.get_json()
    id_item = int(data.get("id_item"))

    cart_cookie = request.cookies.get("cart")
    cart = json.loads(cart_cookie) if cart_cookie else []

    for item in cart:
        if item["id_item"] == id_item:
            if item["amount"] > 1:
                item["amount"] -= 1
                item["price"] = item["amount"] * item["unit_price"]
            else:
                cart.remove(item)
            break

    response = make_response(jsonify({"success": True}))
    response.set_cookie("cart", json.dumps(cart), max_age=MAX_AGE_COOKIE)
    return response
