"""Componente: Validação.

Funções simples para validar dados recebidos pelas APIs.
Interface pública: non_empty_text, positive_int, positive_number, require_json_fields.
"""

from components.errors import ValidationError


def non_empty_text(value, field):
    """Garante que o valor é um texto não vazio e devolve o texto sem espaços nas pontas."""
    text = str(value or "").strip()
    if not text:
        raise ValidationError(f"O campo '{field}' é obrigatório.")
    return text


def positive_int(value, field):
    """Converte para inteiro e garante que é maior que zero."""
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise ValidationError(f"O campo '{field}' deve ser um número inteiro.")
    if number <= 0:
        raise ValidationError(f"O campo '{field}' deve ser maior que zero.")
    return number


def positive_number(value, field):
    """Converte para float e garante que é maior que zero."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValidationError(f"O campo '{field}' deve ser numérico.")
    if number <= 0:
        raise ValidationError(f"O campo '{field}' deve ser maior que zero.")
    return number


def require_json_fields(data, fields):
    """Garante que o corpo JSON existe e contém todos os campos pedidos."""
    if not isinstance(data, dict):
        raise ValidationError("Corpo da requisição deve ser um JSON.")
    for field in fields:
        if field not in data:
            raise ValidationError(f"O campo '{field}' é obrigatório.")
    return data
