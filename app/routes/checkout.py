from flask import Blueprint, request, jsonify, render_template, make_response, session
from app.services.queries import get_orders_by_table_checkout, update_item_by_order_status

checkout_bp = Blueprint("/restaurant", __name__)

@checkout_bp.route("/restaurant/checkout", methods=["GET", "POST"])
def checkout():
    if session.get("user_id") is None:
        return make_response(render_template("login.html"), 401)

    if request.method == "POST":
        if request.form.get("action") == "update_status":
            order_ids = request.form.get("order_ids", []).split(",")
            new_status = request.form.get("new_status")
            table_number = request.form.get("table_number")

            if not table_number:
                return make_response(jsonify({"error": "Missing table_number"}), 400)
            if not new_status:
                return make_response(jsonify({"error": "Missing new_status"}), 400)
            if not order_ids or order_ids == ['']:
                return make_response(jsonify({"error": "No orders selected"}), 400)

            for id_order in order_ids:
                update_item_by_order_status(id_order, new_status)
            orders = get_orders_by_table_checkout(table_number)
            return render_template("checkout.html", active="checkout", orders=orders, success="Order status updated successfully")

        table_number = request.form.get("table_number")
        if not table_number:
            return make_response(render_template("checkout.html", active="checkout", error="Table number is required"), 400)
        orders = get_orders_by_table_checkout(table_number)
        return render_template("checkout.html", active="checkout", orders=orders)
    
    return render_template("checkout.html", active="checkout") 