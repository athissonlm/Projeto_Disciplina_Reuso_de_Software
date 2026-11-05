"""Cart Service - regras de negócio.

O carrinho guarda só (product_id, quantidade). Nome e preço vêm do
Catalog Service via HTTP: é a comunicação entre microsserviços.

Componentes reutilizados: http_client, pricing, validation.
"""

from components import http_client, pricing, validation
from config import SERVICE_URLS
from services.cart_service import repository


def _buscar_produto(product_id):
    """Chama o Catalog Service. Levanta erro 404 se o produto não existir."""
    return http_client.get(f"{SERVICE_URLS['catalog']}/products/{product_id}")


def get_cart(cart_id):
    itens = []
    for linha in repository.get_items(cart_id):
        produto = _buscar_produto(linha["product_id"])
        itens.append({
            "product_id": produto["id"],
            "name": produto["name"],
            "price": produto["price"],
            "quantity": linha["quantity"],
            "subtotal": pricing.subtotal(produto["price"], linha["quantity"]),
        })

    return {
        "cart_id": cart_id,
        "items": itens,
        "total_items": sum(item["quantity"] for item in itens),
        "total": pricing.calculate_total(itens),
    }


def add_item(cart_id, product_id, quantity=1):
    product_id = validation.positive_int(product_id, "product_id")
    quantity = validation.positive_int(quantity, "quantity")

    _buscar_produto(product_id)  # garante que o produto existe
    repository.add_item(cart_id, product_id, quantity)
    return get_cart(cart_id)


def remove_item(cart_id, product_id):
    repository.remove_item(cart_id, product_id)
    return get_cart(cart_id)


def clear_cart(cart_id):
    repository.clear(cart_id)
    return get_cart(cart_id)
