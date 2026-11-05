"""Payment Service - camada de dados (tabela: payments)."""

from components.database import execute, query_one


def save_payment(order_id, amount, method, status, message):
    payment_id = execute(
        "INSERT INTO payments (order_id, amount, method, status, message) VALUES (?, ?, ?, ?, ?)",
        (order_id, amount, method, status, message),
    )
    return get_payment(payment_id)


def get_payment(payment_id):
    return query_one(
        "SELECT id, order_id, amount, method, status, message, created_at FROM payments WHERE id = ?",
        (payment_id,),
    )
