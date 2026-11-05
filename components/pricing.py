"""Componente: Preços.

Interface pública:
    subtotal(price, quantity)  -> preço * quantidade
    calculate_total(items)     -> soma dos subtotais de uma lista de itens

Cada item é um dict com as chaves "price" e "quantity".
"""


def subtotal(price, quantity):
    return round(float(price) * int(quantity), 2)


def calculate_total(items):
    return round(sum(subtotal(item["price"], item["quantity"]) for item in items), 2)
