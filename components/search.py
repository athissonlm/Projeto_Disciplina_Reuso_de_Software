"""Componente: Busca.

Interface (contrato):  ISearcher
Implementações:        LinearSearcher, BinarySearcher

Atalhos em forma de função:
    busca_linear(lista, termo, campo="name")   -> itens cujo campo CONTÉM o termo
    busca_binaria(lista, termo, campo="name")  -> itens cujo campo COMEÇA com o termo

Exemplo de componente usando outro componente: BinarySearcher recebe um
ISorter (por padrão, o BubbleSorter) para ordenar a lista antes de buscar.
"""

from abc import ABC, abstractmethod

from components.sorting import BubbleSorter, ISorter


def _normalizar(valor):
    return str(valor or "").strip().lower()


class ISearcher(ABC):
    """Interface do componente de busca."""

    @abstractmethod
    def search(self, lista, termo, campo="name"):
        """Devolve os itens da lista que casam com o termo."""


class LinearSearcher(ISearcher):
    def search(self, lista, termo, campo="name"):
        """Percorre a lista inteira (O(n)) procurando o termo dentro do campo."""
        termo = _normalizar(termo)
        if not termo:
            return []
        return [item for item in lista if termo in _normalizar(item.get(campo))]


class BinarySearcher(ISearcher):
    def __init__(self, sorter: ISorter = None):
        self.sorter = sorter or BubbleSorter()

    def search(self, lista, termo, campo="name"):
        """Busca binária (O(log n)) pelo primeiro item cujo campo começa com o termo.

        A busca binária exige lista ORDENADA, então ordenamos antes (com o sorter).
        Depois achamos a primeira posição possível e coletamos os vizinhos que
        também começam com o termo.
        """
        termo = _normalizar(termo)
        if not termo:
            return []

        ordenada = self.sorter.sort(lista, key=lambda item: _normalizar(item.get(campo)))
        valores = [_normalizar(item.get(campo)) for item in ordenada]

        # Limite inferior: primeira posição onde valores[pos] >= termo
        esquerda, direita = 0, len(valores)
        while esquerda < direita:
            meio = (esquerda + direita) // 2
            if valores[meio] < termo:
                esquerda = meio + 1
            else:
                direita = meio

        resultados = []
        posicao = esquerda
        while posicao < len(valores) and valores[posicao].startswith(termo):
            resultados.append(ordenada[posicao])
            posicao += 1
        return resultados


# Instâncias padrão + atalhos em forma de função
busca_linear = LinearSearcher().search
busca_binaria = BinarySearcher().search
