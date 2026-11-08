"""APLICAÇÃO 1 — Loja de Eletrônicos (E-commerce Online).

Reusa o framework implementando APENAS os hotspots da classe
EcommerceApplication. O controle da compra usa o FluxoDeCompra padrão
(total = soma dos itens, sem regras extras).

Hotspots implementados:
    nome_loja()          -> "E-commerce Online"
    metodos_pagamento()  -> pix, cartão e boleto
    limite_pagamento()   -> R$ 5.000,00 (acima disso o pagamento é recusado)
"""

from framework.application import EcommerceApplication


class LojaEletronicos(EcommerceApplication):
    def nome_loja(self):
        return "E-commerce Online"

    def metodos_pagamento(self):
        return ("pix", "cartao", "boleto")

    def limite_pagamento(self):
        return 5000.0


def criar_aplicacao():
    return LojaEletronicos()
