"""Catalog Service - camada de dados (tabela: products)."""

from components.database import query_all, query_one

COLUNAS = "id, name, description, price, image"


def get_all_products():
    return query_all(f"SELECT {COLUNAS} FROM products")


def get_product_by_id(product_id):
    return query_one(f"SELECT {COLUNAS} FROM products WHERE id = ?", (product_id,))
