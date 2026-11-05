"""Order Service (porta 5003) - API REST de pedidos.

Endpoints:
    GET  /health
    GET  /orders
    GET  /orders/<id>
    POST /orders    corpo: {"cart_id": "...", "customer_name": "Ana", "payment_method": "pix"}
"""

from flask import jsonify, request

from components.database import ensure_database
from components.service_app import create_service_app, run_service
from components.validation import require_json_fields
from config import PORTS
from services.order_service import service

ensure_database()
app = create_service_app("order-service")


@app.get("/orders")
def list_orders():
    return jsonify({"orders": service.list_orders()})


@app.get("/orders/<int:order_id>")
def get_order(order_id):
    return jsonify(service.get_order(order_id))


@app.post("/orders")
def create_order():
    data = require_json_fields(
        request.get_json(silent=True), ["cart_id", "customer_name", "payment_method"]
    )
    order = service.create_order(data["cart_id"], data["customer_name"], data["payment_method"])
    return jsonify(order), 201


if __name__ == "__main__":
    run_service(app, PORTS["order"])
