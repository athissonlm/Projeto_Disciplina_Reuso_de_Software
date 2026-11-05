"""Frontend (porta 5000) - interface web do e-commerce.

Não tem regra de negócio nem acesso ao banco: apenas monta as páginas
chamando os microsserviços por HTTP (catálogo, carrinho e pedidos).
O carrinho do visitante é identificado por um cart_id guardado na sessão.
"""

import uuid

from flask import Flask, flash, redirect, render_template, request, session, url_for

from components import http_client
from components.errors import AppError
from config import HOST, PAYMENT_METHODS, PORTS, SECRET_KEY, SERVICE_URLS

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

CATALOG = SERVICE_URLS["catalog"]
CART = SERVICE_URLS["cart"]
ORDER = SERVICE_URLS["order"]


def current_cart_id():
    if "cart_id" not in session:
        session["cart_id"] = uuid.uuid4().hex
    return session["cart_id"]


@app.errorhandler(AppError)
def handle_app_error(error):
    return render_template("error.html", message=error.message, status=error.status_code), error.status_code


@app.route("/")
def home():
    data = http_client.get(f"{CATALOG}/products")
    return render_template("homepage.html", produtos=data["products"], total=data["total"])


@app.route("/catalog")
def catalog():
    q = request.args.get("q", "").strip()
    metodo = request.args.get("metodo", "linear")
    ordenacao = request.args.get("ordenacao", "price_asc")

    data = http_client.get(
        f"{CATALOG}/products",
        params={"q": q, "metodo": metodo, "ordenacao": ordenacao},
    )
    return render_template(
        "crafts.html",
        produtos=data["products"],
        total=data["total"],
        q=q,
        metodo=metodo,
        ordenacao=ordenacao,
    )


@app.route("/product/<int:product_id>")
def product_page(product_id):
    try:
        produto = http_client.get(f"{CATALOG}/products/{product_id}")
    except AppError as error:
        if error.status_code == 404:
            return render_template("productpage.html", produto=None, product_id=product_id), 404
        raise
    return render_template("productpage.html", produto=produto, product_id=product_id)


@app.route("/cart")
def cart():
    data = http_client.get(f"{CART}/carts/{current_cart_id()}")
    return render_template("cart.html", cart=data)


@app.route("/cart/add", methods=["POST"])
def add_to_cart():
    product_id = request.form.get("product_id")
    quantity = request.form.get("quantity", 1)
    http_client.post(
        f"{CART}/carts/{current_cart_id()}/items",
        json={"product_id": product_id, "quantity": quantity},
    )
    flash("Produto adicionado ao carrinho.", "success")
    return redirect(url_for("cart"))


@app.route("/cart/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    http_client.delete(f"{CART}/carts/{current_cart_id()}/items/{product_id}")
    return redirect(url_for("cart"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart_id = current_cart_id()

    if request.method == "POST":
        order = http_client.post(
            f"{ORDER}/orders",
            json={
                "cart_id": cart_id,
                "customer_name": request.form.get("customer_name", ""),
                "payment_method": request.form.get("payment_method", ""),
            },
        )
        if order["status"] == "paid":
            flash(f"Pedido #{order['id']} pago com sucesso!", "success")
            return redirect(url_for("orders"))
        flash(f"Pagamento recusado: {order['payment']['message']} Pedido #{order['id']} não foi pago.", "error")
        return redirect(url_for("checkout"))

    data = http_client.get(f"{CART}/carts/{cart_id}")
    if not data["items"]:
        flash("Seu carrinho está vazio.", "error")
        return redirect(url_for("cart"))
    return render_template("checkout.html", cart=data, payment_methods=PAYMENT_METHODS)


@app.route("/orders")
def orders():
    data = http_client.get(f"{ORDER}/orders")
    return render_template("orders.html", orders=data["orders"])


if __name__ == "__main__":
    print(f"[frontend] rodando em http://{HOST}:{PORTS['frontend']}")
    app.run(host=HOST, port=PORTS["frontend"], debug=False)
