"""API Gateway (porta 5005) - ponto de entrada único dos microsserviços.

O frontend (e qualquer cliente externo) fala SÓ com o gateway; ele
encaminha cada requisição ao microsserviço certo, pelo prefixo da rota.

Endpoints:
    GET     /health
    GET     /api/services                    lista os serviços, portas e status (online/offline)
    GET|POST|DELETE /api/<servico>/<caminho> encaminha para o serviço

Tabela de roteamento (servico -> destino):
    /api/catalog/...  ->  Catalog Service  (5001)    ex.: /api/catalog/products     -> GET /products
    /api/cart/...     ->  Cart Service     (5002)    ex.: /api/cart/carts/abc       -> GET /carts/abc
    /api/order/...    ->  Order Service    (5003)    ex.: /api/order/orders         -> GET /orders
    /api/payment/...  ->  Payment Service  (5004)    ex.: /api/payment/payments     -> POST /payments

Componentes reutilizados: service_app, http_client, errors.
"""

from flask import jsonify, request

from components import http_client
from components.errors import AppError, NotFoundError
from components.service_app import create_service_app, run_service
from config import PORTS, SERVICE_URLS

app = create_service_app("api-gateway")

# chave da rota -> (nome amigável, chave em config.PORTS / SERVICE_URLS)
SERVICOS = {
    "catalog": "Catalog Service",
    "cart": "Cart Service",
    "order": "Order Service",
    "payment": "Payment Service",
}


@app.get("/api/services")
def listar_servicos():
    """Consulta o /health de cada serviço e devolve nome, porta, URL e status."""
    lista = [{
        "name": "API Gateway", "key": "gateway", "port": PORTS["gateway"],
        "url": SERVICE_URLS["gateway"], "status": "online",
    }]
    for chave, nome in SERVICOS.items():
        try:
            http_client.get(f"{SERVICE_URLS[chave]}/health")
            status = "online"
        except AppError:
            status = "offline"
        lista.append({
            "name": nome, "key": chave, "port": PORTS[chave],
            "url": SERVICE_URLS[chave], "status": status,
        })
    return jsonify({"services": lista})


@app.route("/api/<servico>/<path:caminho>", methods=["GET", "POST", "DELETE"])
def encaminhar(servico, caminho):
    if servico not in SERVICOS:
        raise NotFoundError(f"Serviço '{servico}' não existe no gateway.")

    destino = f"{SERVICE_URLS[servico]}/{caminho}"
    if request.method == "GET":
        dados, codigo = http_client.get(destino, params=request.args.to_dict()), 200
    elif request.method == "POST":
        dados, codigo = http_client.post(destino, json=request.get_json(silent=True)), 201
    else:
        dados, codigo = http_client.delete(destino), 200
    return jsonify(dados), codigo


if __name__ == "__main__":
    run_service(app, PORTS["gateway"])
