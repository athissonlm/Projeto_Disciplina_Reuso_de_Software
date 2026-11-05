"""Componente: Fábrica de microsserviço.

Todo microsserviço do projeto nasce daqui. A fábrica entrega uma aplicação
Flask já com:
    - rota GET /health (para saber se o serviço está vivo)
    - tratamento padrão de erros, sempre respondendo JSON {"error": "..."}

Interface pública: create_service_app(nome), run_service(app, porta)
"""

from flask import Flask, jsonify

from components.errors import AppError
from config import HOST


def create_service_app(service_name):
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


def run_service(app, port):
    print(f"[{app.name}] rodando em http://{HOST}:{port}")
    app.run(host=HOST, port=port, debug=False)
