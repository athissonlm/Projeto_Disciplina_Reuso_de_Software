"""Componente: Validação.

Interface (contrato):  IValidador
Implementação:         Validador

Funções simples para validar dados recebidos pelas APIs.
Para quem prefere funções, o módulo também expõe atalhos que usam uma
instância padrão: non_empty_text, positive_int, positive_number, require_json_fields.
"""

from abc import ABC, abstractmethod

from components.errors import ValidationError


class IValidador(ABC):
    """Interface do componente de validação."""

    @abstractmethod
    def non_empty_text(self, value, field):
        """Texto não vazio (devolve o texto sem espaços nas pontas)."""

    @abstractmethod
    def positive_int(self, value, field):
        """Inteiro maior que zero."""

    @abstractmethod
    def positive_number(self, value, field):
        """Número (float) maior que zero."""

    @abstractmethod
    def require_json_fields(self, data, fields):
        """Corpo JSON com todos os campos pedidos."""


class Validador(IValidador):
    def non_empty_text(self, value, field):
        """Garante que o valor é um texto não vazio e devolve o texto sem espaços nas pontas."""
        text = str(value or "").strip()
        if not text:
            raise ValidationError(f"O campo '{field}' é obrigatório.")
        return text

    def positive_int(self, value, field):
        """Converte para inteiro e garante que é maior que zero."""
        try:
            number = int(value)
        except (TypeError, ValueError):
            raise ValidationError(f"O campo '{field}' deve ser um número inteiro.")
        if number <= 0:
            raise ValidationError(f"O campo '{field}' deve ser maior que zero.")
        return number

    def positive_number(self, value, field):
        """Converte para float e garante que é maior que zero."""
        try:
            number = float(value)
        except (TypeError, ValueError):
            raise ValidationError(f"O campo '{field}' deve ser numérico.")
        if number <= 0:
            raise ValidationError(f"O campo '{field}' deve ser maior que zero.")
        return number

    def require_json_fields(self, data, fields):
        """Garante que o corpo JSON existe e contém todos os campos pedidos."""
        if not isinstance(data, dict):
            raise ValidationError("Corpo da requisição deve ser um JSON.")
        for field in fields:
            if field not in data:
                raise ValidationError(f"O campo '{field}' é obrigatório.")
        return data


# Instância padrão + atalhos em forma de função
_padrao = Validador()
non_empty_text = _padrao.non_empty_text
positive_int = _padrao.positive_int
positive_number = _padrao.positive_number
require_json_fields = _padrao.require_json_fields
