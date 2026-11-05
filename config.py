"""Configuração central do projeto.

Aqui ficam os caminhos do banco de dados e o "registro de serviços":
a lista de quem roda em qual porta. Um serviço descobre o endereço dos
outros consultando SERVICE_URLS.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# --- Banco de dados (SQLite) -------------------------------------------
DB_PATH = BASE_DIR / "database" / "ecommerce.db"
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"
SEED_PATH = BASE_DIR / "database" / "seed.sql"

# --- Registro de serviços ----------------------------------------------
HOST = "127.0.0.1"

PORTS = {
    "frontend": 5000,
    "catalog": 5001,
    "cart": 5002,
    "order": 5003,
    "payment": 5004,
}

SERVICE_URLS = {nome: f"http://{HOST}:{porta}" for nome, porta in PORTS.items()}

# --- Frontend ----------------------------------------------------------
SECRET_KEY = "ecommerce-framework-secret"  # usado pela sessão (cookie do carrinho)

# --- Regra de negócio do Payment Service (simulado) --------------------
PAYMENT_METHODS = ("pix", "cartao", "boleto")
PAYMENT_LIMIT = 5000.0  # pagamentos acima disso são recusados (para demonstrar falha)
