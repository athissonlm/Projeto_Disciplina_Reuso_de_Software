"""Order Service - camada de dados (tabelas: orders, order_items)."""

from components.database import connection, execute, query_all, query_one


def create_order(customer_name, total, items):
    """Grava o pedido e seus itens na mesma transação (ou grava tudo, ou nada)."""
    with connection() as conn:
        cursor = conn.execute(
            "INSERT INTO orders (customer_name, total) VALUES (?, ?)",
            (customer_name, total),
        )
        order_id = cursor.lastrowid
        for item in items:
            conn.execute(
                "INSERT INTO order_items (order_id, product_id, product_name, unit_price, quantity) "
                "VALUES (?, ?, ?, ?, ?)",
                (order_id, item["product_id"], item["name"], item["price"], item["quantity"]),
            )
    return order_id


def update_status(order_id, status):
    execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))


def get_order(order_id):
    order = query_one(
        "SELECT id, customer_name, total, status, created_at FROM orders WHERE id = ?",
        (order_id,),
    )
    if order:
        order["items"] = query_all(
            "SELECT product_id, product_name, unit_price, quantity FROM order_items WHERE order_id = ?",
            (order_id,),
        )
    return order


def list_orders():
    ids = query_all("SELECT id FROM orders ORDER BY id DESC")
    return [get_order(row["id"]) for row in ids]
