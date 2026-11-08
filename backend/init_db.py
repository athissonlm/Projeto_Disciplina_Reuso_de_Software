"""Inicializa o banco de dados SQLite da aplicação escolhida.

Uso (a partir da raiz do projeto):
    python backend/init_db.py                       # cria o banco se necessário
    python backend/init_db.py --reset               # apaga e recria tudo do zero
    python backend/init_db.py --app livraria        # escolhe a aplicação (padrão: loja_eletronicos)
"""

import os
import sys
from pathlib import Path

# Permite rodar o script direto, sem precisar de "python -m".
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

if "--app" in sys.argv:  # precisa ser definido ANTES de importar o config
    os.environ["ECOMMERCE_APP"] = sys.argv[sys.argv.index("--app") + 1]

from components.database import init_database  # noqa: E402
from config import DB_PATH  # noqa: E402


if __name__ == "__main__":
    reset = "--reset" in sys.argv
    init_database(reset=reset)
    print(f"Banco pronto em: {DB_PATH}" + (" (recriado)" if reset else ""))
