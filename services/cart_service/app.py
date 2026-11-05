"""Cart Service (porta 5002) - API REST do carrinho.

Endpoints:
    GET    /health
    GET    /carts/<cart_id>
    POST   /carts/<cart_id>/items            corpo: {"product_id": 1, "quantity": 2}
    DELETE /carts/<cart_id>/items/<product_id>
    DELETE /carts/<cart_id>                  esvazia o carrinho
"""

from flask import jsonify, request

from components.database import ensure_database
from components.service_app import create_service_app, run_service
from components.validation import require_json_fields
from config import PORTS
from services.cart_service import service

ensure_database()
app = create_service_app("cart-service")


@app.get("/carts/<cart_id>")
def get_cart(cart_id):
    return jsonify(service.get_cart(cart_id))


@app.post("/carts/<cart_id>/items")
def add_item(cart_id):
    data = require_json_fields(request.get_json(silent=True), ["product_id"])
    cart = service.add_item(cart_id, data["product_id"], data.get("quantity", 1))
    return jsonify(cart), 201


@app.delete("/carts/<cart_id>/items/<int:product_id>")
def remove_item(cart_id, product_id):
    return jsonify(service.remove_item(cart_id, product_id))


@app.delete("/carts/<cart_id>")
def clear_cart(cart_id):
    return jsonify(service.clear_cart(cart_id))


if __name__ == "__main__":
    run_service(app, PORTS["cart"])
