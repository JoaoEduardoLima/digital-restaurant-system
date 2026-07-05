from flask import Blueprint, request, jsonify, render_template, make_response
from app.services.queries import get_items
from app.services.utils import MAX_AGE_COOKIE

menu_bp = Blueprint("menu", __name__)

@menu_bp.route("/menu", methods=["GET"])
def menu():
    if request.method == 'GET':
        table_number = request.args.get("table") or request.cookies.get("table_number")
        if not table_number:
            return jsonify({"error": "Miss table number"}), 400
        else:
            items = get_items()
            response = make_response(render_template("menu.html", items=items, active='menu'))
            response.set_cookie("table_number", table_number, max_age=MAX_AGE_COOKIE)
            return response
