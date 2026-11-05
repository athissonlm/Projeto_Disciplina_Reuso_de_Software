"""Inicializa o banco de dados SQLite do projeto.

Uso (a partir da raiz do projeto):
    python database/init_db.py           # cria o banco se necessário
    python database/init_db.py --reset   # apaga e recria tudo do zero
"""

import sys
from pathlib import Path

# Permite rodar o script direto, sem precisar de "python -m".
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from components.database import init_database  # noqa: E402
from config import DB_PATH  # noqa: E402


if __name__ == "__main__":
    reset = "--reset" in sys.argv
    init_database(reset=reset)
    print(f"Banco pronto em: {DB_PATH}" + (" (recriado)" if reset else ""))
