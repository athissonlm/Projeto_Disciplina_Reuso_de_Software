"""APLICAÇÃO 2 — Livraria Online.

Reusa o framework implementando hotspots da classe EcommerceApplication E
do controle da compra (subclasse de FluxoDeCompra).

Hotspots implementados:
    EcommerceApplication.nome_loja()          -> "Livraria Online"
    EcommerceApplication.metodos_pagamento()  -> só pix e cartão
    EcommerceApplication.limite_pagamento()   -> R$ 1.500,00
    EcommerceApplication.criar_fluxo_de_compra() -> devolve FluxoLivraria

    FluxoDeCompra.validar_pedido()   -> pedido mínimo de R$ 20,00
    FluxoDeCompra.calcular_total()   -> soma dos itens + frete de R$ 12,00 (grátis a partir de R$ 150,00)
    FluxoDeCompra.apos_pagamento()   -> avisa a expedição quando o pedido é pago
"""

from components import pricing
from components.errors import ValidationError
from framework.application import EcommerceApplication
from framework.fluxo_de_compra import FluxoDeCompra


class FluxoLivraria(FluxoDeCompra):
    PEDIDO_MINIMO = 20.0
    FRETE = 12.0
    FRETE_GRATIS_A_PARTIR_DE = 150.0

    def validar_pedido(self, carrinho):  # HOTSPOT 1
        subtotal = pricing.calculate_total(carrinho["items"])
        if subtotal < self.PEDIDO_MINIMO:
            raise ValidationError(f"Pedido mínimo da livraria: R$ {self.PEDIDO_MINIMO:.2f}.")

    def calcular_total(self, itens):  # HOTSPOT 2
        subtotal = super().calcular_total(itens)  # reaproveita o cálculo padrão
        frete = 0.0 if subtotal >= self.FRETE_GRATIS_A_PARTIR_DE else self.FRETE
        return round(subtotal + frete, 2)

    def apos_pagamento(self, pedido):  # HOTSPOT 3
        if pedido["status"] == "paid":
            print(f"[livraria] Pedido #{pedido['id']} pago: avisar a expedição para separar os livros.")


class Livraria(EcommerceApplication):
    def nome_loja(self):
        return "Livraria Online"

    def metodos_pagamento(self):
        return ("pix", "cartao")

    def limite_pagamento(self):
        return 1500.0

    def criar_fluxo_de_compra(self, repositorio, http=None):
        return FluxoLivraria(self, repositorio, http)


def criar_aplicacao():
    return Livraria()
