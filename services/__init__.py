"""MICROSSERVIÇOS do framework de e-commerce.

Cada subpasta é um microsserviço independente (processo e porta próprios),
sempre com a mesma estrutura de 3 camadas:
    app.py         -> API REST (rotas HTTP)
    service.py     -> regras de negócio
    repository.py  -> acesso aos dados (tabelas que pertencem ao serviço)

    catalog_service  (porta 5001) -> produtos
    cart_service     (porta 5002) -> carrinho
    order_service    (porta 5003) -> pedidos
    payment_service  (porta 5004) -> pagamentos
"""
