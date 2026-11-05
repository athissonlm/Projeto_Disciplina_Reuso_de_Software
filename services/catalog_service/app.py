"""Catalog Service (porta 5001) - API REST de produtos.

Endpoints:
    GET /health
    GET /products?q=&metodo=linear|binaria&ordenacao=price_asc|price_desc|name_asc|name_desc
    GET /products/<id>
"""

from flask import jsonify, request

from components.database import ensure_database
from components.service_app import create_service_app, run_service
from config import PORTS
from services.catalog_service import service

ensure_database()
app = create_service_app("catalog-service")


@app.get("/products")
def list_products():
    produtos = service.list_products(
        q=request.args.get("q", "").strip(),
        metodo=request.args.get("metodo", "linear"),
        ordenacao=request.args.get("ordenacao", "price_asc"),
    )
    return jsonify({"total": len(produtos), "products": produtos})


@app.get("/products/<int:product_id>")
def get_product(product_id):
    return jsonify(service.get_product(product_id))


if __name__ == "__main__":
    run_service(app, PORTS["catalog"])
