"""Componente: Ordenação.

Interface (contrato):  ISorter
Implementação:         BubbleSorter

Atalho em forma de função: bubble_sort(lista, key=None, reverse=False)
"""

from abc import ABC, abstractmethod


class ISorter(ABC):
    """Interface do componente de ordenação."""

    @abstractmethod
    def sort(self, lista, key=None, reverse=False):
        """Devolve uma NOVA lista ordenada."""


class BubbleSorter(ISorter):
    def sort(self, lista, key=None, reverse=False):
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


# Instância padrão + atalho em forma de função
_padrao = BubbleSorter()
bubble_sort = _padrao.sort
