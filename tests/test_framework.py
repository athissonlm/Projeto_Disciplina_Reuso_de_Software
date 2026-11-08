"""Testes do FRAMEWORK (Template Method + hotspots) e das duas aplicações.

Não precisam de Flask, banco nem serviços no ar: usamos um cliente HTTP
falso e um repositório em memória (injeção de dependência).
"""

import pytest

from apps.livraria.application import FluxoLivraria, Livraria
from apps.loja_eletronicos.application import LojaEletronicos
from components.errors import ValidationError
from config import SERVICE_URLS
from framework.fluxo_de_compra import FluxoDeCompra


class HttpFalso:
    def __init__(self, itens, status_pagamento="approved"):
        self.itens = itens
        self.status_pagamento = status_pagamento
        self.chamadas = []

    def get(self, url, params=None):
        self.chamadas.append(("GET", url))
        return {"items": self.itens}

    def post(self, url, json=None):
        self.chamadas.append(("POST", url))
        return {"status": self.status_pagamento, "message": "ok"}

    def delete(self, url):
        self.chamadas.append(("DELETE", url))
        return {}


class RepositorioFalso:
    def __init__(self):
        self.pedido = None

    def create_order(self, nome, total, itens):
        self.pedido = {"id": 1, "customer_name": nome, "total": total, "status": "created"}
        return 1

    def update_status(self, order_id, status):
        self.pedido["status"] = status

    def get_order(self, order_id):
        return dict(self.pedido)


def item(preco, qtd=1):
    return {"product_id": 1, "name": "X", "price": preco, "quantity": qtd}


def test_fluxo_padrao_soma_itens_e_esvazia_carrinho():
    http = HttpFalso([item(100.0, 2)])
    fluxo = LojaEletronicos().criar_fluxo_de_compra(RepositorioFalso(), http)

    pedido = fluxo.executar("c1", "Ana", "pix")

    assert type(fluxo) is FluxoDeCompra
    assert pedido["total"] == 200.0
    assert pedido["status"] == "paid"
    assert ("DELETE", f"{SERVICE_URLS['cart']}/carts/c1") in http.chamadas


def test_pagamento_recusado_nao_esvazia_carrinho():
    http = HttpFalso([item(100.0)], status_pagamento="refused")
    fluxo = LojaEletronicos().criar_fluxo_de_compra(RepositorioFalso(), http)

    pedido = fluxo.executar("c1", "Ana", "pix")

    assert pedido["status"] == "payment_failed"
    assert not any(metodo == "DELETE" for metodo, _ in http.chamadas)


def test_metodo_de_pagamento_depende_da_aplicacao():
    http = HttpFalso([item(100.0)])
    # boleto existe na loja de eletrônicos, mas não na livraria
    LojaEletronicos().criar_fluxo_de_compra(RepositorioFalso(), http).executar("c1", "Ana", "boleto")
    with pytest.raises(ValidationError):
        Livraria().criar_fluxo_de_compra(RepositorioFalso(), http).executar("c1", "Ana", "boleto")


def test_carrinho_vazio_e_recusado():
    fluxo = LojaEletronicos().criar_fluxo_de_compra(RepositorioFalso(), HttpFalso([]))
    with pytest.raises(ValidationError):
        fluxo.executar("c1", "Ana", "pix")


def test_livraria_usa_subclasse_do_fluxo():
    assert isinstance(Livraria().criar_fluxo_de_compra(RepositorioFalso()), FluxoLivraria)


def test_livraria_hotspot_frete():
    fluxo = FluxoLivraria(Livraria(), RepositorioFalso(), HttpFalso([]))
    assert fluxo.calcular_total([item(100.0)]) == 112.0   # frete de R$ 12,00
    assert fluxo.calcular_total([item(150.0)]) == 150.0   # frete grátis


def test_livraria_hotspot_pedido_minimo():
    fluxo = FluxoLivraria(Livraria(), RepositorioFalso(), HttpFalso([item(10.0)]))
    with pytest.raises(ValidationError):
        fluxo.executar("c1", "Ana", "pix")


def test_orcamento_mostra_total_com_hotspot():
    fluxo = FluxoLivraria(Livraria(), RepositorioFalso(), HttpFalso([item(100.0)]))
    assert fluxo.orcamento("c1") == {"subtotal": 100.0, "total": 112.0}


def test_hotspots_de_pagamento_das_aplicacoes():
    assert LojaEletronicos().limite_pagamento() == 5000.0
    assert Livraria().limite_pagamento() == 1500.0
    assert Livraria().nome_loja() == "Livraria Online"
