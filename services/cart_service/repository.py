"""Cart Service - camada de dados (tabela: cart_items)."""

from components.database import execute, query_all


def get_items(cart_id):
    return query_all(
        "SELECT product_id, quantity FROM cart_items WHERE cart_id = ? ORDER BY id",
        (cart_id,),
    )


def add_item(cart_id, product_id, quantity):
    """Insere o item; se já existir no carrinho, soma a quantidade."""
    execute(
        "INSERT INTO cart_items (cart_id, product_id, quantity) VALUES (?, ?, ?) "
        "ON CONFLICT (cart_id, product_id) DO UPDATE SET quantity = quantity + excluded.quantity",
        (cart_id, product_id, quantity),
    )


def remove_item(cart_id, product_id):
    execute(
        "DELETE FROM cart_items WHERE cart_id = ? AND product_id = ?",
        (cart_id, product_id),
    )


def clear(cart_id):
    execute("DELETE FROM cart_items WHERE cart_id = ?", (cart_id,))
