import json

from flask import Blueprint, redirect, request, make_response
from app.services.utils import MAX_AGE_COOKIE

cart_bp = Blueprint('cart', __name__)

@cart_bp.route("/cart", methods=["POST"])
def cart():
    table_number = request.form.get("table_number")
    id_item = int(request.form.get("id_item"))
    name = request.form.get("name")
    price = float(request.form.get("price"))
    note = request.form.get("note")
    amount = 1

    cart_cookie = request.cookies.get("cart")
    cart = json.loads(cart_cookie) if cart_cookie else []



    for item in cart:
        if item["id_item"] == id_item and item["note"] == note:
            item["amount"] += 1
            item["price"] = item["amount"] * item["unit_price"]
            break
    else:
        cart.append({
            "id_item": id_item,
            "name": name,
            "unit_price": price,
            "price": price,
            "note": note,
            "amount": amount
        })

    response = make_response(redirect("/order"))
    response.set_cookie("cart", json.dumps(cart), max_age=MAX_AGE_COOKIE)
    return response
