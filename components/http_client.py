"""Componente: Cliente HTTP.

É assim que os microsserviços conversam entre si. Se o serviço chamado
estiver fora do ar ou devolver erro, levantamos uma AppError com o código
HTTP apropriado, e o erro sobe de forma padronizada.

Interface pública: get(url, params=None), post(url, json=None), delete(url)
"""

import requests

from components.errors import AppError

TIMEOUT = 5  # segundos


def _request(method, url, **kwargs):
    try:
        response = requests.request(method, url, timeout=TIMEOUT, **kwargs)
    except requests.RequestException:
        raise AppError(f"Serviço indisponível: {url}", 503)

    try:
        data = response.json()
    except ValueError:
        data = {}

    if response.status_code >= 400:
        message = data.get("error") if isinstance(data, dict) else None
        raise AppError(message or f"Erro {response.status_code} ao chamar {url}", response.status_code)

    return data


def get(url, params=None):
    return _request("GET", url, params=params)


def post(url, json=None):
    return _request("POST", url, json=json)


def delete(url):
    return _request("DELETE", url)
