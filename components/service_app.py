"""Componente: Fábrica de microsserviço.

Interface (contrato):  IServiceFactory
Implementação:         ServiceAppFactory

Todo microsserviço do projeto nasce daqui. A fábrica entrega uma aplicação
Flask já com:
    - rota GET /health (para saber se o serviço está vivo)
    - tratamento padrão de erros, sempre respondendo JSON {"error": "..."}

Atalhos em forma de função: create_service_app(nome), run_service(app, porta)
"""

from abc import ABC, abstractmethod

from flask import Flask, jsonify

from components.errors import AppError
from config import HOST


class IServiceFactory(ABC):
    """Interface do componente fábrica de microsserviço."""

    @abstractmethod
    def create(self, service_name):
        """Cria a aplicação Flask padrão de um microsserviço."""

    @abstractmethod
    def run(self, app, port):
        """Sobe o servidor do microsserviço na porta indicada."""


class ServiceAppFactory(IServiceFactory):
    def __init__(self, host=HOST):
        self.host = host

    def create(self, service_name):
        app = Flask(service_name)
        app.json.ensure_ascii = False  # mantém acentos no JSON

        @app.get("/health")
        def health():
            return jsonify({"service": service_name, "status": "ok"})

        @app.errorhandler(AppError)
        def handle_app_error(error):
            return jsonify({"error": error.message}), error.status_code

        @app.errorhandler(404)
        def handle_not_found(_error):
            return jsonify({"error": "Rota não encontrada."}), 404

        @app.errorhandler(405)
        def handle_method_not_allowed(_error):
            return jsonify({"error": "Método não permitido."}), 405

        return app

    def run(self, app, port):
        print(f"[{app.name}] rodando em http://{self.host}:{port}")
        app.run(host=self.host, port=port, debug=False)


# Instância padrão + atalhos em forma de função
_padrao = ServiceAppFactory()
create_service_app = _padrao.create
run_service = _padrao.run
