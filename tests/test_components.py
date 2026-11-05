"""Testes dos COMPONENTES reutilizáveis (não precisam de Flask nem de banco)."""

import pytest

from components.errors import ValidationError
from components.pricing import calculate_total, subtotal
from components.search import busca_binaria, busca_linear
from components.sorting import bubble_sort
from components.validation import positive_int

PRODUTOS = [
    {"name": "Mouse", "price": 170.0},
    {"name": "Fone", "price": 200.0},
    {"name": "Notebook", "price": 3000.0},
    {"name": "Mouse Gamer", "price": 250.0},
]


def test_bubble_sort_crescente_e_decrescente():
    precos = [p["price"] for p in bubble_sort(PRODUTOS, key=lambda p: p["price"])]
    assert precos == [170.0, 200.0, 250.0, 3000.0]

    precos = [p["price"] for p in bubble_sort(PRODUTOS, key=lambda p: p["price"], reverse=True)]
    assert precos == [3000.0, 250.0, 200.0, 170.0]


def test_bubble_sort_nao_altera_a_lista_original():
    original = list(PRODUTOS)
    bubble_sort(PRODUTOS, key=lambda p: p["price"])
    assert PRODUTOS == original


def test_busca_linear_encontra_trecho_do_nome():
    assert [p["name"] for p in busca_linear(PRODUTOS, "gamer")] == ["Mouse Gamer"]
    assert busca_linear(PRODUTOS, "") == []


def test_busca_binaria_encontra_nomes_que_comecam_com_o_termo():
    nomes = [p["name"] for p in busca_binaria(PRODUTOS, "mou")]
    assert nomes == ["Mouse", "Mouse Gamer"]
    assert busca_binaria(PRODUTOS, "gamer") == []


def test_pricing():
    assert subtotal(10.5, 2) == 21.0
    assert calculate_total([{"price": 10.5, "quantity": 2}, {"price": 3, "quantity": 1}]) == 24.0


def test_validation_positive_int():
    assert positive_int("3", "quantity") == 3
    with pytest.raises(ValidationError):
        positive_int(0, "quantity")
    with pytest.raises(ValidationError):
        positive_int("abc", "quantity")
