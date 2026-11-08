"""Componente: Cliente HTTP.

Interface (contrato):  IHttpClient
Implementação:         HttpClient

É assim que os microsserviços conversam entre si. Se o serviço chamado
estiver fora do ar ou devolver erro, levantamos uma AppError com o código
HTTP apropriado, e o erro sobe de forma padronizada.

Atalhos em forma de função: get(url, params=None), post(url, json=None), delete(url)
`default_client` é a instância padrão (útil para injetar um cliente falso nos testes).
"""

from abc import ABC, abstractmethod

import requests

from components.errors import AppError


class IHttpClient(ABC):
    """Interface do componente de cliente HTTP."""

    @abstractmethod
    def get(self, url, params=None):
        """GET; devolve o JSON da resposta."""

    @abstractmethod
    def post(self, url, json=None):
        """POST com corpo JSON; devolve o JSON da resposta."""

    @abstractmethod
    def delete(self, url):
        """DELETE; devolve o JSON da resposta."""


class HttpClient(IHttpClient):
    def __init__(self, timeout=5):
        self.timeout = timeout  # segundos

    def _request(self, method, url, **kwargs):
        try:
            response = requests.request(method, url, timeout=self.timeout, **kwargs)
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

    def get(self, url, params=None):
        return self._request("GET", url, params=params)

    def post(self, url, json=None):
        return self._request("POST", url, json=json)

    def delete(self, url):
        return self._request("DELETE", url)


# Instância padrão + atalhos em forma de função
default_client = HttpClient()
get = default_client.get
post = default_client.post
delete = default_client.delete
