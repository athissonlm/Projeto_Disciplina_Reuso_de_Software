"""Configuração central do projeto.

Aqui ficam os caminhos do banco de dados e o "registro de serviços":
a lista de quem roda em qual porta. Um serviço descobre o endereço dos
outros consultando SERVICE_URLS.

APLICAÇÃO ATIVA
    O framework pode rodar diferentes aplicações (ex.: loja_eletronicos, livraria).
    A escolhida vem da variável de ambiente ECOMMERCE_APP (o main.py define
    isso com `python main.py --app livraria`). Cada aplicação tem o seu
    próprio banco (backend/<aplicacao>.db) e seus dados iniciais
    (apps/<aplicacao>/seed.sql).
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# --- Aplicação ativa -----------------------------------------------------
APP_NAME = os.environ.get("ECOMMERCE_APP", "loja_eletronicos")

# --- Banco de dados (SQLite) -------------------------------------------
DB_PATH = BASE_DIR / "backend" / f"{APP_NAME}.db"
SCHEMA_PATH = BASE_DIR / "backend" / "schema.sql"
SEED_PATH = BASE_DIR / "apps" / APP_NAME / "seed.sql"

# --- Registro de serviços ----------------------------------------------
HOST = "127.0.0.1"

PORTS = {
    "frontend": 5000,
    "catalog": 5001,
    "cart": 5002,
    "order": 5003,
    "payment": 5004,
    "gateway": 5005,
}

SERVICE_URLS = {nome: f"http://{HOST}:{porta}" for nome, porta in PORTS.items()}

# --- Frontend ----------------------------------------------------------
SECRET_KEY = "ecommerce-framework-secret"  # usado pela sessão (cookie do carrinho)

# As regras de pagamento (métodos aceitos e limite) NÃO ficam mais aqui:
# são HOTSPOTS da aplicação (ver framework/application.py e apps/*/application.py).
