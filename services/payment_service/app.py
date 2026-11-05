"""Payment Service (porta 5004) - API REST de pagamentos.

Endpoints:
    GET  /health
    POST /payments    corpo: {"order_id": 1, "amount": 200.0, "method": "pix"}
"""

from flask import jsonify, request

from components.database import ensure_database
from components.service_app import create_service_app, run_service
from components.validation import require_json_fields
from config import PORTS
from services.payment_service import service

ensure_database()
app = create_service_app("payment-service")


@app.post("/payments")
def create_payment():
    data = require_json_fields(request.get_json(silent=True), ["order_id", "amount", "method"])
    payment = service.process_payment(data["order_id"], data["amount"], data["method"])
    return jsonify(payment), 201


if __name__ == "__main__":
    run_service(app, PORTS["payment"])
