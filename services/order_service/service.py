"""Order Service - regras de negócio.

O fluxo de compra (orquestração entre Cart, Payment e este serviço) vem do
FRAMEWORK: classe FluxoDeCompra (padrão Template Method). A aplicação ativa
decide qual subclasse usar (hotspots) em criar_fluxo_de_compra().

Este módulo só liga o framework ao repositório de pedidos.
"""

from components.errors import NotFoundError
from framework.loader import get_application
from services.order_service import repository

fluxo = get_application().criar_fluxo_de_compra(repository)


def create_order(cart_id, customer_name, payment_method):
    return fluxo.executar(cart_id, customer_name, payment_method)


def quote(cart_id):
    """Subtotal e total que seria cobrado (com frete/descontos da aplicação)."""
    return fluxo.orcamento(cart_id)


def get_order(order_id):
    order = repository.get_order(order_id)
    if order is None:
        raise NotFoundError(f"Pedido {order_id} não encontrado.")
    return order


def list_orders():
    return repository.list_orders()
