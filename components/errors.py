"""Componente: Erros.

Exceções padronizadas. Qualquer microsserviço que levantar uma AppError
terá a resposta convertida automaticamente em JSON (ver service_app.py).
"""


class AppError(Exception):
    """Erro de aplicação com um código HTTP associado."""

    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ValidationError(AppError):
    """Dados de entrada inválidos (HTTP 400)."""

    def __init__(self, message):
        super().__init__(message, 400)


class NotFoundError(AppError):
    """Recurso não encontrado (HTTP 404)."""

    def __init__(self, message):
        super().__init__(message, 404)
