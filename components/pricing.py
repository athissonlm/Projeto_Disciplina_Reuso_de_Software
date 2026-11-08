"""Componente: Preços.

Interface (contrato):  IPriceCalculator
Implementação:         PriceCalculator

Atalhos em forma de função:
    subtotal(price, quantity)  -> preço * quantidade
    calculate_total(items)     -> soma dos subtotais de uma lista de itens

Cada item é um dict com as chaves "price" e "quantity".
"""

from abc import ABC, abstractmethod


class IPriceCalculator(ABC):
    """Interface do componente de preços."""

    @abstractmethod
    def subtotal(self, price, quantity):
        """Preço unitário * quantidade."""

    @abstractmethod
    def calculate_total(self, items):
        """Soma dos subtotais dos itens."""


class PriceCalculator(IPriceCalculator):
    def subtotal(self, price, quantity):
        return round(float(price) * int(quantity), 2)

    def calculate_total(self, items):
        return round(sum(self.subtotal(item["price"], item["quantity"]) for item in items), 2)


# Instância padrão + atalhos em forma de função
_padrao = PriceCalculator()
subtotal = _padrao.subtotal
calculate_total = _padrao.calculate_total
