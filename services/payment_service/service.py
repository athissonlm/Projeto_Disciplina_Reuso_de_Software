"""Payment Service - regras de negócio (pagamento SIMULADO).

Regras didáticas:
    - o método de pagamento deve ser um de PAYMENT_METHODS
    - valores acima de PAYMENT_LIMIT são recusados (para demonstrar o fluxo de falha)

Componentes reutilizados: validation, errors.
"""

from components import validation
from components.errors import ValidationError
from config import PAYMENT_LIMIT, PAYMENT_METHODS
from services.payment_service import repository


def process_payment(order_id, amount, method):
    order_id = validation.positive_int(order_id, "order_id")
    amount = validation.positive_number(amount, "amount")
    method = validation.non_empty_text(method, "method").lower()

    if method not in PAYMENT_METHODS:
        raise ValidationError(f"Método de pagamento inválido. Use: {', '.join(PAYMENT_METHODS)}.")

    if amount > PAYMENT_LIMIT:
        status, message = "refused", f"Valor acima do limite de R$ {PAYMENT_LIMIT:.2f}."
    else:
        status, message = "approved", "Pagamento aprovado."

    return repository.save_payment(order_id, amount, method, status, message)
