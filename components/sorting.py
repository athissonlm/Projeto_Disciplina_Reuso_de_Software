"""Componente: Ordenação.

Interface pública: bubble_sort(lista, key=None, reverse=False)
"""


def bubble_sort(lista, key=None, reverse=False):
    """Ordena uma lista com Bubble Sort e devolve uma NOVA lista.

    key     -> função que extrai o valor a comparar (ex.: lambda p: p["price"])
    reverse -> True para ordem decrescente
    """
    if key is None:
        key = lambda item: item

    itens = list(lista)  # cópia: não altera a lista original
    n = len(itens)

    for i in range(n):
        trocou = False
        for j in range(n - i - 1):
            a, b = key(itens[j]), key(itens[j + 1])
            fora_de_ordem = (a < b) if reverse else (a > b)
            if fora_de_ordem:
                itens[j], itens[j + 1] = itens[j + 1], itens[j]
                trocou = True
        if not trocou:  # já está ordenada
            break

    return itens
