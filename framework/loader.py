"""Carrega a aplicação ativa.

Convenção: a aplicação "xyz" vive em apps/xyz/application.py e oferece a
função criar_aplicacao() que devolve uma EcommerceApplication.
A escolha vem de config.APP_NAME (variável de ambiente ECOMMERCE_APP).
"""

import importlib
from functools import lru_cache

from config import APP_NAME


@lru_cache(maxsize=1)
def get_application():
    try:
        modulo = importlib.import_module(f"apps.{APP_NAME}.application")
    except ImportError as erro:
        raise RuntimeError(
            f"Aplicação '{APP_NAME}' não encontrada. Verifique se existe apps/{APP_NAME}/application.py."
        ) from erro
    return modulo.criar_aplicacao()
