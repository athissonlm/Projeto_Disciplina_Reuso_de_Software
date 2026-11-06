# Framework para Sistemas de E-commerce
### Microsserviços + Componentes de Software Reutilizáveis

Projeto acadêmico que mostra, de forma **didática e simples**, como organizar um e-commerce em **microsserviços** e **componentes reutilizáveis**.

Disciplina: Reuso de Software e Metodologias Ágeis  
Discentes: Athisson Alberto Lima Marques e Pedro Henrique Santos da Silva  
Docente: Arturo Hernandez Dominguez

---

## 1. Ideia central

O projeto separa duas coisas que costumam ficar misturadas:

| Conceito | O que é neste projeto | Onde fica |
|---|---|---|
| **Microsserviço** | Um mini-sistema independente: roda em seu próprio processo e porta, tem sua API REST e seus próprios dados. Resolve **um** problema de negócio. | `services/` |
| **Componente de software** | Uma peça pequena e reutilizável (busca, ordenação, banco, validação...). **Não conhece** nenhum serviço específico, então vários serviços podem usá-la. | `components/` |

> Em resumo: **serviços** respondem *"o que o negócio faz"* (catálogo, carrinho, pedido, pagamento); **componentes** respondem *"com o que os serviços são construídos"* (as peças que se repetem).

---

## 2. Arquitetura

```text
                         ┌──────────────────────────┐
                         │   Frontend  (porta 5000) │   páginas HTML (Flask + Jinja)
                         └─────────────┬────────────┘
                                       │ HTTP
        ┌──────────────────────────────┼───────────────────────────┐
        ▼                              ▼                           ▼
┌────────────────┐            ┌────────────────┐           ┌────────────────┐
│ Catalog Service│◄───────────│  Cart Service  │           │  Order Service │
│  porta 5001    │   HTTP     │   porta 5002   │◄──────────│   porta 5003   │
│  products      │            │   cart_items   │   HTTP    │ orders         │
└────────────────┘            └────────────────┘           │ order_items    │
                                                           └───────┬────────┘
                                                                   │ HTTP
                                                           ┌───────▼────────┐
                                                           │Payment Service │
                                                           │  porta 5004    │
                                                           │  payments      │
                                                           └────────────────┘

        ┌────────────────────────────────────────────────────────────┐
        │  components/  (usados por TODOS os serviços acima)         │
        │  errors · validation · sorting · search · pricing ·        │
        │  database · http_client · service_app                      │
        └────────────────────────────────────────────────────────────┘

                        backend/ecommerce.db  (SQLite)
```

Regras da arquitetura:

1. **Cada serviço tem seu processo e sua porta** e só se comunica com os outros **por HTTP** (nunca importando o código do vizinho).
2. **Cada tabela pertence a um único serviço.** Só ele lê e escreve nela. Por isso não há chaves estrangeiras entre tabelas de serviços diferentes.
3. **Todo serviço tem as mesmas 3 camadas** (`app.py` → `service.py` → `repository.py`).
4. **Componentes nunca dependem de um serviço.** A dependência é sempre *serviço → componente*.

---

## 3. Microsserviços

Todos seguem o mesmo molde:

```text
services/<nome>_service/
├── app.py          # API REST: define as rotas HTTP e chama o service.py
├── service.py      # Regras de negócio
└── repository.py   # Acesso ao banco (apenas as tabelas deste serviço)
```

### 3.1 Catalog Service — porta 5001
Lista, busca e ordena produtos. Tabela: `products`.

| Método | Rota | Descrição |
|---|---|---|
| GET | `/health` | Verifica se o serviço está no ar |
| GET | `/products?q=&metodo=&ordenacao=` | Lista produtos. `metodo`: `linear` ou `binaria`. `ordenacao`: `price_asc`, `price_desc`, `name_asc`, `name_desc` |
| GET | `/products/<id>` | Detalhe de um produto |

### 3.2 Cart Service — porta 5002
Guarda os itens de cada carrinho (`product_id` + quantidade). Para mostrar nome e preço, **chama o Catalog Service**. Tabela: `cart_items`.

| Método | Rota | Descrição |
|---|---|---|
| GET | `/carts/<cart_id>` | Itens, subtotais e total do carrinho |
| POST | `/carts/<cart_id>/items` | Adiciona item `{"product_id": 1, "quantity": 2}` |
| DELETE | `/carts/<cart_id>/items/<product_id>` | Remove um item |
| DELETE | `/carts/<cart_id>` | Esvazia o carrinho |

### 3.3 Order Service — porta 5003
Cria e consulta pedidos. É o serviço que **orquestra a compra**, chamando o Cart e o Payment. Tabelas: `orders` e `order_items`.

| Método | Rota | Descrição |
|---|---|---|
| GET | `/orders` | Lista pedidos |
| GET | `/orders/<id>` | Detalhe de um pedido |
| POST | `/orders` | Cria pedido `{"cart_id": "...", "customer_name": "Ana", "payment_method": "pix"}` |

### 3.4 Payment Service — porta 5004
Processa o pagamento (**simulado**). Tabela: `payments`.

| Método | Rota | Descrição |
|---|---|---|
| POST | `/payments` | `{"order_id": 1, "amount": 200.0, "method": "pix"}` |

Regras simuladas: métodos aceitos são `pix`, `cartao` e `boleto`; valores **acima de R$ 5.000,00 são recusados** (serve para demonstrar o fluxo de falha). Ambos configuráveis em `config.py`.

### 3.5 Frontend — porta 5000
Não tem regra de negócio nem acesso ao banco: só monta as páginas HTML chamando os microsserviços. O carrinho do visitante é identificado por um `cart_id` guardado na sessão (cookie).

---

## 4. Fluxo de compra (comunicação entre serviços)

```text
Cliente clica em "Confirmar pedido"
   │
   ▼
Frontend ──POST /orders──► Order Service
                              │ 1. GET  /carts/<id>   ──► Cart Service ──GET /products/<id>──► Catalog Service
                              │ 2. calcula o total (componente pricing) e grava o pedido
                              │ 3. POST /payments     ──► Payment Service
                              │ 4. atualiza status do pedido: "paid" ou "payment_failed"
                              │ 5. se pago: DELETE /carts/<id> ──► Cart Service (esvazia)
                              ▼
                           resposta ao Frontend
```

Status possíveis do pedido: `created` → `paid` ou `payment_failed`.

---

## 5. Componentes de software reutilizáveis

Ficam em `components/`. Cada um tem uma interface pública pequena e documentada no próprio arquivo.

| Componente | Arquivo | Interface pública | Usado por |
|---|---|---|---|
| Erros | `errors.py` | `AppError`, `ValidationError`, `NotFoundError` | todos |
| Validação | `validation.py` | `non_empty_text`, `positive_int`, `positive_number`, `require_json_fields` | Cart, Order, Payment |
| Ordenação | `sorting.py` | `bubble_sort(lista, key, reverse)` | Catalog, `search` |
| Busca | `search.py` | `busca_linear`, `busca_binaria` | Catalog |
| Preços | `pricing.py` | `subtotal`, `calculate_total` | Cart, Order |
| Banco de dados | `database.py` | `connection`, `query_all`, `query_one`, `execute`, `init_database`, `ensure_database` | todos os serviços |
| Cliente HTTP | `http_client.py` | `get`, `post`, `delete` | Cart, Order, Frontend |
| Fábrica de serviço | `service_app.py` | `create_service_app`, `run_service` | todos os serviços |

**Exemplo de reuso:** o componente `service_app` entrega a todo microsserviço a rota `/health` e o tratamento padrão de erros em JSON. Os quatro serviços usam a mesma chamada, mudando só o nome:

```python
app = create_service_app("catalog-service")
```

Outro exemplo: `search.busca_binaria` reaproveita `sorting.bubble_sort` (componente usando componente).

**Diferença entre as buscas:**
- `busca_linear` percorre toda a lista e encontra nomes que **contêm** o termo (ex.: `gamer` → *Fone Gamer*, *Mouse Gamer*, *Teclado Gamer*).
- `busca_binaria` ordena a lista e usa busca binária para encontrar nomes que **começam com** o termo (ex.: `mou` → *Mouse Gamer*).

---

## 6. Banco de dados

SQLite (um arquivo, sem instalação), criado automaticamente em `backend/ecommerce.db`.

```text
backend/
├── schema.sql    # criação das tabelas
├── seed.sql      # produtos iniciais
└── init_db.py    # script para criar/recriar o banco
```

```text
 Catalog Service         Cart Service           Order Service              Payment Service
┌──────────────┐       ┌──────────────┐       ┌───────────────────┐      ┌───────────────┐
│ products     │       │ cart_items   │       │ orders            │      │ payments      │
│──────────────│       │──────────────│       │───────────────────│      │───────────────│
│ id (PK)      │       │ id (PK)      │       │ id (PK)           │      │ id (PK)       │
│ name         │       │ cart_id      │       │ customer_name     │      │ order_id      │
│ description  │       │ product_id   │       │ total             │      │ amount        │
│ price        │       │ quantity     │       │ status            │      │ method        │
│ image        │       └──────────────┘       │ created_at        │      │ status        │
└──────────────┘                              ├───────────────────┤      │ message       │
                                              │ order_items       │      │ created_at    │
                                              │ order_id (FK)     │      └───────────────┘
                                              │ product_id        │
                                              │ product_name      │
                                              │ unit_price        │
                                              │ quantity          │
                                              └───────────────────┘
```

Pontos importantes:
- `cart_items.product_id`, `order_items.product_id` e `payments.order_id` **não são chaves estrangeiras**: apontam para dados de *outro serviço*, que só se acessa por HTTP.
- `order_items` guarda uma **cópia** do nome e do preço (`product_name`, `unit_price`), assim o histórico não muda se o catálogo for alterado.
- Aqui os 4 serviços usam o **mesmo arquivo SQLite** só para simplificar. Em um sistema real, cada serviço teria seu próprio banco (padrão *database per service*).

---

## 7. Estrutura do projeto

```text
Projeto_Reuso_E-Commerce/
├── components/                 # COMPONENTES reutilizáveis
│   ├── errors.py
│   ├── validation.py
│   ├── sorting.py
│   ├── search.py
│   ├── pricing.py
│   ├── database.py
│   ├── http_client.py
│   └── service_app.py
├── services/                   # MICROSSERVIÇOS
│   ├── catalog_service/        # app.py · service.py · repository.py
│   ├── cart_service/
│   ├── order_service/
│   └── payment_service/
├── frontend/                   # interface web (consome os serviços via HTTP)
│   ├── app.py
│   ├── templates/
│   └── static/
├── backend/                    # banco de dados: schema.sql · seed.sql · init_db.py
├── tests/                      # testes dos componentes
├── config.py                   # portas, URLs dos serviços, caminhos do banco
├── main.py                     # sobe tudo (banco + serviços + frontend)
├── requirements.txt
└── readme.md
```

---

## 8. Tecnologias

- Python 3 e Flask (APIs REST e páginas)
- Jinja2 (templates HTML)
- SQLite (módulo `sqlite3` do Python)
- Requests (chamadas HTTP entre serviços)
- Pytest (testes)

---

## 9. Como executar

```bash
cd Projeto_Reuso_E-Commerce
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

O `main.py` cria o banco (se necessário) e inicia os 5 processos.

**Subir só um serviço**:

```bash
python -m services.catalog_service.app
```

**Recriar o banco do zero**:

```bash
python backend/init_db.py --reset
```

### Testando as APIs diretamente

Com tudo rodando, cada serviço responde por conta própria:

```bash
curl http://127.0.0.1:5001/products
curl "http://127.0.0.1:5001/products?q=mou&metodo=binaria"
curl http://127.0.0.1:5002/health

curl -X POST http://127.0.0.1:5002/carts/teste/items -H "Content-Type: application/json" -d "{\"product_id\": 1, \"quantity\": 2}"
curl http://127.0.0.1:5002/carts/teste

curl -X POST http://127.0.0.1:5003/orders -H "Content-Type: application/json" -d "{\"cart_id\": \"teste\", \"customer_name\": \"Ana\", \"payment_method\": \"pix\"}"
```

### Testes automatizados

```bash
python -m pytest
```

---

## 10. Possíveis evoluções

- Um banco separado para cada serviço
- Autenticação de clientes e histórico de pedidos por usuário
- API Gateway único na frente dos serviços
- Docker / docker-compose para subir cada serviço em um contêiner
- Comunicação assíncrona (fila de mensagens) entre Order e Payment

---

## 11. Conclusão

O projeto mostra, em escala pequena, como **microsserviços** (separação por responsabilidade de negócio, comunicação por HTTP, dados próprios) e **componentes de software** (peças reutilizáveis, independentes dos serviços) se complementam para construir um framework de e-commerce fácil de entender, manter e estender.
