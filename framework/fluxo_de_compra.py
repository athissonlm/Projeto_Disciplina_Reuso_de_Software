"""CONTROLE da compra do framework — padrão de projeto TEMPLATE METHOD.

O que é fixo (igual para toda loja) está no método-template `executar()`:
a ORDEM dos passos da compra e a comunicação com os outros microsserviços.
O que varia de loja para loja são os HOTSPOTS (pontos de adaptação), métodos
que a aplicação sobrescreve em uma subclasse:

    HOTSPOT 1  validar_pedido(carrinho)   regras extras (ex.: pedido mínimo)       [padrão: nada]
    HOTSPOT 2  calcular_total(itens)      política de preço (frete, desconto...)    [padrão: soma dos itens]
    HOTSPOT 3  apos_pagamento(pedido)     ação extra após o pagamento (aviso, log)  [padrão: nada]

Passos do template (✔ = fixo, ★ = hotspot):

    ✔ 1. valida os dados de entrada e o método de pagamento
    ✔ 2. busca o carrinho no Cart Service (HTTP) e garante que não está vazio
    ★ 3. validar_pedido(carrinho)
    ★ 4. calcular_total(itens)
    ✔ 5. grava o pedido
    ✔ 6. cobra no Payment Service (HTTP) e atualiza o status (paid | payment_failed)
    ✔ 7. se pago, esvazia o carrinho no Cart Service (HTTP)
    ★ 8. apos_pagamento(pedido)

O repositório é recebido por INJEÇÃO (é "duck typing": qualquer objeto com
create_order, update_status e get_order). Assim o framework não depende de
nenhum microsserviço específico.
"""

from components import pricing, validation
from components.errors import AppError, ValidationError
from components.http_client import default_client
from config import SERVICE_URLS


class FluxoDeCompra:
    def __init__(self, application, repositorio, http=None):
        """
        application -> EcommerceApplication (fornece métodos de pagamento etc.)
        repositorio -> objeto com create_order(nome, total, itens), update_status(id, status), get_order(id)
        http        -> cliente HTTP (IHttpClient); por padrão usa o componente http_client
        """
        self.application = application
        self.repositorio = repositorio
        self.http = http or default_client

    # ------------------------------------------------------------------
    # TEMPLATE METHOD: define o esqueleto da compra. Não sobrescreva!
    # ------------------------------------------------------------------
    def executar(self, cart_id, customer_name, payment_method):
        # 1. entrada
        cart_id = validation.non_empty_text(cart_id, "cart_id")
        customer_name = validation.non_empty_text(customer_name, "customer_name")
        payment_method = validation.non_empty_text(payment_method, "payment_method").lower()
        self._validar_metodo_pagamento(payment_method)

        # 2. carrinho
        carrinho = self._buscar_carrinho(cart_id)
        if not carrinho["items"]:
            raise ValidationError("O carrinho está vazio.")

        self.validar_pedido(carrinho)                      # HOTSPOT 1
        total = self.calcular_total(carrinho["items"])     # HOTSPOT 2

        # 5. grava o pedido
        order_id = self.repositorio.create_order(customer_name, total, carrinho["items"])

        # 6. pagamento
        pagamento = self._cobrar(order_id, total, payment_method)
        status = "paid" if pagamento["status"] == "approved" else "payment_failed"
        self.repositorio.update_status(order_id, status)

        # 7. esvazia o carrinho se pago
        if status == "paid":
            self.http.delete(f"{SERVICE_URLS['cart']}/carts/{cart_id}")

        pedido = self.repositorio.get_order(order_id)
        pedido["payment"] = pagamento

        self.apos_pagamento(pedido)                        # HOTSPOT 3
        return pedido

    # ------------------------------------------------------------------
    # HOTSPOTS: a aplicação sobrescreve o que precisar
    # ------------------------------------------------------------------
    def validar_pedido(self, carrinho):
        """HOTSPOT 1 — regras extras antes de criar o pedido. Levante ValidationError para recusar."""

    def calcular_total(self, itens):
        """HOTSPOT 2 — total do pedido. Padrão: soma dos subtotais dos itens."""
        return pricing.calculate_total(itens)

    def apos_pagamento(self, pedido):
        """HOTSPOT 3 — ação extra depois do pagamento (ex.: avisar a expedição)."""

    # ------------------------------------------------------------------
    # Consulta de valores (usada pelo checkout para mostrar o total real)
    # ------------------------------------------------------------------
    def orcamento(self, cart_id):
        """Devolve o subtotal dos itens e o total que SERIA cobrado (com os hotspots aplicados)."""
        cart_id = validation.non_empty_text(cart_id, "cart_id")
        itens = self._buscar_carrinho(cart_id)["items"]
        return {"subtotal": pricing.calculate_total(itens), "total": self.calcular_total(itens)}

    # ------------------------------------------------------------------
    # Passos fixos (privados)
    # ------------------------------------------------------------------
    def _validar_metodo_pagamento(self, metodo):
        permitidos = self.application.metodos_pagamento()
        if metodo not in permitidos:
            raise ValidationError(f"Método de pagamento inválido. Use: {', '.join(permitidos)}.")

    def _buscar_carrinho(self, cart_id):
        return self.http.get(f"{SERVICE_URLS['cart']}/carts/{cart_id}")

    def _cobrar(self, order_id, total, metodo):
        try:
            return self.http.post(
                f"{SERVICE_URLS['payment']}/payments",
                json={"order_id": order_id, "amount": total, "method": metodo},
            )
        except AppError:
            self.repositorio.update_status(order_id, "payment_failed")
            raise
