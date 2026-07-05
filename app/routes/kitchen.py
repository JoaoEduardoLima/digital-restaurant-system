from flask import Blueprint, request, jsonify, render_template, make_response, session
from app.services.queries import get_orders, update_order_status
from app.services.utils import group_orders_by_id

kitchen_bp = Blueprint("kitchen", __name__)

@kitchen_bp.route("/restaurant/kitchen", methods=["GET", "POST"])
def kitchen():
    if session.get("user_id") is None:
        return make_response(render_template("login.html"), 401)

    if request.method == "POST":
        # Atualizar status do pedido
        order_id = request.form.get("order_id")
        new_status = request.form.get("new_status")

        if not order_id or not new_status:
            return jsonify({"error": "Missing order_id or new_status"}), 400

        result = update_order_status(order_id, new_status)
        if "error" in result:
            return jsonify(result), 400

        orders = get_orders()
        orders_by_id = group_orders_by_id(orders)

        return render_template("kitchen.html", active="kitchen", orders=orders_by_id, message="Order status updated successfully.")

    # GET normal → renderiza página inicial
    orders = get_orders()
    orders_by_id = group_orders_by_id(orders)
    return render_template("kitchen.html", active="kitchen", orders=orders_by_id)

