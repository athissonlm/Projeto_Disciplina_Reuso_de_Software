"""Catalog Service - regras de negócio.

Componentes reutilizados: sorting (Bubble Sort), search (linear/binária), errors.
"""

from components.errors import NotFoundError
from components.search import busca_binaria, busca_linear
from components.sorting import bubble_sort
from services.catalog_service import repository

# ordenação -> (função que extrai o valor, ordem decrescente?)
ORDENACOES = {
    "price_asc": (lambda p: p["price"], False),
    "price_desc": (lambda p: p["price"], True),
    "name_asc": (lambda p: p["name"].lower(), False),
    "name_desc": (lambda p: p["name"].lower(), True),
}


def list_products(q="", metodo="linear", ordenacao="price_asc"):
    produtos = repository.get_all_products()

    chave, decrescente = ORDENACOES.get(ordenacao, ORDENACOES["price_asc"])
    produtos = bubble_sort(produtos, key=chave, reverse=decrescente)

    if q:
        if metodo == "binaria":
            produtos = busca_binaria(produtos, q)
        else:
            produtos = busca_linear(produtos, q)

    return produtos


def get_product(product_id):
    produto = repository.get_product_by_id(product_id)
    if produto is None:
        raise NotFoundError(f"Produto {product_id} não encontrado.")
    return produto
