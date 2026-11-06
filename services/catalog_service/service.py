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

    # 1) filtra pela busca (se houver termo)
    if q:
        if metodo == "binaria":
            produtos = busca_binaria(produtos, q)
        else:
            produtos = busca_linear(produtos, q)

    # 2) ordena o resultado pelo critério escolhido (vale para qualquer método de busca)
    chave, decrescente = ORDENACOES.get(ordenacao, ORDENACOES["price_asc"])
    return bubble_sort(produtos, key=chave, reverse=decrescente)


def get_product(product_id):
    produto = repository.get_product_by_id(product_id)
    if produto is None:
        raise NotFoundError(f"Produto {product_id} não encontrado.")
    return produto
