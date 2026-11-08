"""A CLASSE DO FRAMEWORK: EcommerceApplication.

Toda aplicação construída com o framework herda desta classe e implementa
os HOTSPOTS (pontos de adaptação):

    nome_loja()                       OBRIGATÓRIO  nome mostrado no site
    metodos_pagamento()               opcional     formas de pagamento aceitas   [padrão: pix, cartao, boleto]
    limite_pagamento()                opcional     valor máximo aprovado         [padrão: R$ 5.000,00]
    criar_fluxo_de_compra(...)        opcional     devolve o CONTROLE da compra  [padrão: FluxoDeCompra]

Os hotspots do controle da compra (validar_pedido, calcular_total,
apos_pagamento) ficam em FluxoDeCompra (framework/fluxo_de_compra.py).
Para trocá-los, a aplicação cria uma subclasse de FluxoDeCompra e a devolve
em criar_fluxo_de_compra().
"""

from abc import ABC, abstractmethod

from framework.fluxo_de_compra import FluxoDeCompra


class EcommerceApplication(ABC):
    # ---- HOTSPOT obrigatório -------------------------------------------
    @abstractmethod
    def nome_loja(self):
        """Nome da loja, exibido no cabeçalho do site."""

    # ---- HOTSPOTS opcionais (têm comportamento padrão) -------------------
    def metodos_pagamento(self):
        """Formas de pagamento aceitas (usadas pelo Order e pelo Payment Service)."""
        return ("pix", "cartao", "boleto")

    def limite_pagamento(self):
        """Pagamentos acima deste valor são recusados (Payment Service, simulado)."""
        return 5000.0

    def criar_fluxo_de_compra(self, repositorio, http=None):
        """Devolve o controle da compra. Sobrescreva para usar uma subclasse de FluxoDeCompra."""
        return FluxoDeCompra(self, repositorio, http)
