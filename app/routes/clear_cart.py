from flask import Blueprint, jsonify, make_response

clear_cart_bp = Blueprint('clear_cart', __name__)

@clear_cart_bp.route("/clear_cart", methods=["POST"])
def clear_cart():
    response = make_response(jsonify({"success": True}))
    response.set_cookie("cart", "", max_age=0)
    return response