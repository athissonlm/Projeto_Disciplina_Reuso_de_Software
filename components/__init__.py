"""COMPONENTES DE SOFTWARE reutilizáveis do framework de e-commerce.

Um componente aqui é um módulo pequeno, com uma responsabilidade única e
uma interface pública simples (funções documentadas). Ele NÃO conhece
nenhum microsserviço específico, por isso pode ser reaproveitado por
qualquer um deles (reuso).

Componentes disponíveis:
    errors              -> exceções padronizadas (AppError, ValidationError, NotFoundError)
    validation          -> validação de dados de entrada
    sorting             -> ordenação (Bubble Sort)
    search              -> busca linear e binária
    pricing             -> cálculo de subtotais e totais
    database            -> acesso ao banco SQLite (conexão e consultas)
    http_client         -> chamadas HTTP entre microsserviços
    service_app         -> fábrica de aplicação Flask padrão para um microsserviço
"""
