# Framework para Sistemas de E-commerce
### Microsserviços + Componentes de Software Reutilizáveis

Projeto acadêmico que mostra, de forma **didática e simples**, como organizar um e-commerce em **microsserviços** e **componentes reutilizáveis**, e como construir **aplicações diferentes reusando o mesmo framework**.

Disciplina: Reuso de Software e Metodologias Ágeis  
Discentes: Athisson Alberto Lima Marques e Pedro Henrique Santos da Silva  
Docente: Arturo Hernandez Dominguez

---

## 1. Ideia central

| Conceito | O que é neste projeto | Onde fica |
|---|---|---|
| **Microsserviço** | Mini-sistema independente: processo, porta, API REST e dados próprios. | `services/` |
| **API Gateway** | Entrada única: encaminha as chamadas ao serviço certo. | `gateway/` |
| **Componente** | Peça reutilizável com **interface** (`ISorter`, `IDatabase`...), sem conhecer nenhum serviço. | `components/` |
| **Framework** | Classe `EcommerceApplication` + controle `FluxoDeCompra` (**Template Method**) com **hotspots**. | `framework/` |
| **Aplicação** | Loja construída sobre o framework, preenchendo os hotspots. | `apps/` |

---

## 2. Arquitetura

```text
                  ┌──────────────────────────┐
                  │   Frontend  (porta 5000) │
                  └─────────────┬────────────┘
                                │ HTTP
                  ┌─────────────▼────────────┐
                  │  API Gateway (porta 5005)│
                  └─────────────┬────────────┘
        ┌───────────────┬───────┴───────┬────────────────┐
        ▼               ▼               ▼                ▼
 Catalog (5001)   Cart (5002)     Order (5003)     Payment (5004)
                                       │ usa FluxoDeCompra (Template Method)

 components/  → usados por todos        framework/ + apps/ → hotspots
 backend/<aplicacao>.db (SQLite)
```

Regras: cada serviço tem seu processo/porta e só fala com os outros por HTTP; cada tabela pertence a um único serviço; todo serviço tem as camadas `app.py` → `service.py` → `repository.py`; dependência é sempre *serviço → componente*.

---

## 3. Microsserviços e Gateway

| Serviço | Porta | Rotas principais |
|---|---|---|
| Catalog | 5001 | `GET /products?q=&metodo=linear\|binaria&ordenacao=`, `GET /products/<id>` |
| Cart | 5002 | `GET /carts/<id>`, `POST /carts/<id>/items`, `DELETE /carts/<id>/items/<pid>`, `DELETE /carts/<id>` |
| Order | 5003 | `GET /orders`, `GET /orders/<id>`, `GET /orders/quote/<cart_id>`, `POST /orders` |
| Payment | 5004 | `POST /payments` |
| API Gateway | 5005 | `/api/<catalog\|cart\|order\|payment>/<rota>`, `GET /api/services` |
| Frontend | 5000 | páginas HTML: catálogo, carrinho, checkout e pedidos |

Todos têm `GET /health`. O frontend usa **somente** o gateway.

**Fluxo de compra:** Frontend → Gateway → Order Service (`FluxoDeCompra.executar`) → Cart (itens) → [hotspots] → Payment → Cart (esvazia se pago).

---

## 4. Framework e hotspots

`framework/fluxo_de_compra.py` define o **método-template** `executar()` (ordem fixa dos passos) e os pontos de adaptação:

| Hotspot | Onde | Padrão |
|---|---|---|
| `nome_loja()` (obrigatório) | `EcommerceApplication` | — |
| `metodos_pagamento()` | `EcommerceApplication` | pix, cartão, boleto |
| `limite_pagamento()` | `EcommerceApplication` | R$ 5.000,00 |
| `criar_fluxo_de_compra()` | `EcommerceApplication` | `FluxoDeCompra` |
| `validar_pedido(carrinho)` | `FluxoDeCompra` | nenhuma regra |
| `calcular_total(itens)` | `FluxoDeCompra` | soma dos itens |
| `apos_pagamento(pedido)` | `FluxoDeCompra` | nada |

## 5. Aplicações

| Aplicação | Comando | Hotspots implementados |
|---|---|---|
| **Loja de Eletrônicos** | `python main.py` | nome, métodos e limite de pagamento |
| **Livraria Online** | `python main.py --app livraria` | + pedido mínimo, frete, aviso de expedição |

Rode **uma por vez** (usam as mesmas portas). Cada uma tem seu banco (`backend/<aplicacao>.db`) e seus produtos (`apps/<aplicacao>/seed.sql`).

### Criar uma nova aplicação

1. Criar `apps/<nome>/` com `__init__.py` (vazio), `seed.sql` (produtos) e `application.py`.
2. Em `application.py`, herdar `EcommerceApplication`, implementar `nome_loja()` e, se quiser, os outros hotspots; expor `criar_aplicacao()`:

```python
from framework.application import EcommerceApplication

class LojaRoupas(EcommerceApplication):
    def nome_loja(self):
        return "Loja de Roupas"

def criar_aplicacao():
    return LojaRoupas()
```

3. (Opcional) Para personalizar a compra, criar uma subclasse de `FluxoDeCompra` (sobrescrevendo `validar_pedido`, `calcular_total` ou `apos_pagamento`) e devolvê-la em `criar_fluxo_de_compra()` — veja `apps/livraria/application.py`.
4. Executar: `python main.py --app <nome>`.

---

## 6. Componentes de software

| Componente | Arquivo | Interface | Implementação |
|---|---|---|---|
| Erros | `errors.py` | — | `AppError`, `ValidationError`, `NotFoundError` |
| Validação | `validation.py` | `IValidador` | `Validador` |
| Ordenação | `sorting.py` | `ISorter` | `BubbleSorter` |
| Busca | `search.py` | `ISearcher` | `LinearSearcher`, `BinarySearcher` |
| Preços | `pricing.py` | `IPriceCalculator` | `PriceCalculator` |
| Banco de dados | `database.py` | `IDatabase` | `SQLiteDatabase` |
| Cliente HTTP | `http_client.py` | `IHttpClient` | `HttpClient` |
| Fábrica de serviço | `service_app.py` | `IServiceFactory` | `ServiceAppFactory` |

Cada módulo também expõe atalhos em função (`bubble_sort`, `query_all`, `http_client.get`...).

---

## 7. Banco de dados

SQLite criado automaticamente em `backend/<aplicacao>.db` (`schema.sql` + `apps/<aplicacao>/seed.sql`). Tabelas: `products` (Catalog), `cart_items` (Cart), `orders` e `order_items` (Order), `payments` (Payment). Sem chaves estrangeiras entre serviços diferentes. Os 4 serviços compartilham o arquivo só para simplificar.

---

## 8. Estrutura do projeto

```text
Projeto_Reuso_E-Commerce/
├── components/     # componentes (interfaces + implementações)
├── framework/      # EcommerceApplication, FluxoDeCompra (Template Method), loader
├── apps/           # loja_eletronicos/ e livraria/ (application.py + seed.sql)
├── services/       # catalog, cart, order, payment (app · service · repository)
├── gateway/        # API Gateway
├── frontend/       # interface web (via gateway)
├── backend/        # schema.sql · init_db.py (bancos .db gerados)
├── tests/          # testes dos componentes e do framework/aplicações
├── config.py · main.py · requirements.txt · pytest.ini
```

---

## 9. Tecnologias

Python 3, Flask, Jinja2, SQLite, Requests, Pytest.

## 10. Como executar

```bash
cd Projeto_Reuso_E-Commerce
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py                   # ou: python main.py --app livraria
```

Acesse http://127.0.0.1:5000.

Um serviço isolado: `python -m services.catalog_service.app`  
Recriar o banco: `python backend/init_db.py --reset [--app livraria]`  
Testes: `python -m pytest`

Exemplos de API (via gateway):

```bash
curl "http://127.0.0.1:5005/api/catalog/products?q=mou&metodo=binaria"
curl http://127.0.0.1:5005/api/services     # serviços, portas e status (JSON)
```
