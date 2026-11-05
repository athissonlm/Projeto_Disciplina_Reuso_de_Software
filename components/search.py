"""Componente: Busca.

Interface pública:
    busca_linear(lista, termo, campo="name")   -> itens cujo campo CONTÉM o termo
    busca_binaria(lista, termo, campo="name")  -> itens cujo campo COMEÇA com o termo
"""

from components.sorting import bubble_sort


def _normalizar(valor):
    return str(valor or "").strip().lower()


def busca_linear(lista, termo, campo="name"):
    """Percorre a lista inteira (O(n)) procurando o termo dentro do campo."""
    termo = _normalizar(termo)
    if not termo:
        return []
    return [item for item in lista if termo in _normalizar(item.get(campo))]


def busca_binaria(lista, termo, campo="name"):
    """Busca binária (O(log n)) pelo primeiro item cujo campo começa com o termo.

    A busca binária exige lista ORDENADA, então ordenamos antes (Bubble Sort).
    Depois achamos a primeira posição possível e coletamos os vizinhos que
    também começam com o termo.
    """
    termo = _normalizar(termo)
    if not termo:
        return []

    ordenada = bubble_sort(lista, key=lambda item: _normalizar(item.get(campo)))
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
