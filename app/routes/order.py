import json

from flask import Blueprint, request, jsonify, render_template, redirect, make_response
from app.services.queries import get_item_by_order, try_new_order
from app.services.validation import valid_order
from app.services.utils import group_items_by_customer, MAX_AGE_COOKIE

order_bp = Blueprint("order", __name__)

@order_bp.route("/order", methods=["GET", "POST"])
def order():
    """Show status of order in the kitchen and status of the cart"""
    if request.method == "GET":
        ids_orders = request.cookies.get("ids_orders", [])
        ids_orders = json.loads(ids_orders) if ids_orders else []
        cart = request.cookies.get("cart", [])
        cart = json.loads(cart) if cart else []
        table_number = request.cookies.get("table_number")
        items = []
        if ids_orders:
            for id_order in ids_orders:
                items.extend(get_item_by_order(id_order))
        items = group_items_by_customer(items)
        return render_template("order.html", items=items, cart=cart, table_number=table_number, active="order")
    
    """Send order to Restaurant"""
    if request.method == "POST":
        table_number = request.cookies.get("table_number")
        data = request.get_json()

        valid_data = valid_order(table_number, data)
        if valid_data.get("error"):
            return valid_data["error"], 400
        
        name = data.get("name")
        items = data.get("items")

        new_order = try_new_order(table_number, name, items)
        id_order = new_order.get("id_order")
        status_order = new_order.get("status")

        if id_order:
            if "ids_orders" in request.cookies:
                ids_orders = request.cookies.get("ids_orders", [])
                ids_orders = json.loads(ids_orders) if ids_orders else []
                ids_orders.append(id_order)
            else:
                ids_orders = [id_order]
            
            response = make_response(jsonify({"success": True}))
            response.set_cookie("ids_orders", json.dumps(ids_orders), max_age=MAX_AGE_COOKIE)

            response.set_cookie("cart", "", max_age=MAX_AGE_COOKIE)
            return response

        else:
            return new_order["error"], 500
        