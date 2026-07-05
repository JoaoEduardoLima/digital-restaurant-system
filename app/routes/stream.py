from flask import Blueprint, request, jsonify, render_template, make_response, session, Response, current_app
from app.services.queries import get_orders, update_order_status
from app.services.utils import group_orders_by_id
import time, json

kitchen_stream_bp = Blueprint("kitchen_stream", __name__)

@kitchen_stream_bp.route("/restaurant/kitchen/stream")
def kitchen_stream():
    if session.get("user_id") is None:
        return make_response(render_template("login.html"), 401)

    def event_stream():
        while True:
            orders = get_orders()
            orders_by_id = group_orders_by_id(orders)
            yield f"data: {json.dumps(orders_by_id)}\n\n"
            time.sleep(2)

    return Response(event_stream(), mimetype="text/event-stream")