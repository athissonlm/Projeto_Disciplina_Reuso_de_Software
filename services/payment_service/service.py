"""Payment Service - regras de negócio (pagamento SIMULADO).

Regras didáticas (são HOTSPOTS da aplicação ativa, ver framework/application.py):
    - o método de pagamento deve estar em application.metodos_pagamento()
    - valores acima de application.limite_pagamento() são recusados
      (para demonstrar o fluxo de falha)

Componentes reutilizados: validation, errors.
"""

from components import validation
from components.errors import ValidationError
from framework.loader import get_application
from services.payment_service import repository


def process_payment(order_id, amount, method):
    aplicacao = get_application()

    order_id = validation.positive_int(order_id, "order_id")
    amount = validation.positive_number(amount, "amount")
    method = validation.non_empty_text(method, "method").lower()

    metodos = aplicacao.metodos_pagamento()
    if method not in metodos:
        raise ValidationError(f"Método de pagamento inválido. Use: {', '.join(metodos)}.")

    limite = aplicacao.limite_pagamento()
    if amount > limite:
        status, message = "refused", f"Valor acima do limite de R$ {limite:.2f}."
    else:
        status, message = "approved", "Pagamento aprovado."

    return repository.save_payment(order_id, amount, method, status, message)
