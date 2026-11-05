"""Order Service - regras de negócio.

Este serviço ORQUESTRA o fluxo de compra, conversando com outros serviços:

    1. Cart Service     -> busca os itens do carrinho
    2. (próprio)        -> calcula o total e grava o pedido
    3. Payment Service  -> processa o pagamento
    4. (próprio)        -> atualiza o status do pedido (paid | payment_failed)
    5. Cart Service     -> esvazia o carrinho, se o pagamento foi aprovado

Componentes reutilizados: http_client, pricing, validation, errors.
"""

from components import http_client, pricing, validation
from components.errors import AppError, NotFoundError, ValidationError
from config import PAYMENT_METHODS, SERVICE_URLS
from services.order_service import repository


def create_order(cart_id, customer_name, payment_method):
    cart_id = validation.non_empty_text(cart_id, "cart_id")
    customer_name = validation.non_empty_text(customer_name, "customer_name")
    payment_method = validation.non_empty_text(payment_method, "payment_method").lower()

    if payment_method not in PAYMENT_METHODS:
        raise ValidationError(f"Método de pagamento inválido. Use: {', '.join(PAYMENT_METHODS)}.")

    # 1. Cart Service
    cart = http_client.get(f"{SERVICE_URLS['cart']}/carts/{cart_id}")
    if not cart["items"]:
        raise ValidationError("O carrinho está vazio.")

    # 2. Total + gravação do pedido
    total = pricing.calculate_total(cart["items"])
    order_id = repository.create_order(customer_name, total, cart["items"])

    # 3. Payment Service
    try:
        payment = http_client.post(
            f"{SERVICE_URLS['payment']}/payments",
            json={"order_id": order_id, "amount": total, "method": payment_method},
        )
    except AppError:
        repository.update_status(order_id, "payment_failed")
        raise

    # 4. Status final do pedido
    status = "paid" if payment["status"] == "approved" else "payment_failed"
    repository.update_status(order_id, status)

    # 5. Cart Service
    if status == "paid":
        http_client.delete(f"{SERVICE_URLS['cart']}/carts/{cart_id}")

    order = repository.get_order(order_id)
    order["payment"] = payment
    return order


def get_order(order_id):
    order = repository.get_order(order_id)
    if order is None:
        raise NotFoundError(f"Pedido {order_id} não encontrado.")
    return order


def list_orders():
    return repository.list_orders()
