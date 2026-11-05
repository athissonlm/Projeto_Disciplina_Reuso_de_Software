"""Launcher do projeto: sobe o banco, os 4 microsserviços e o frontend.

Uso:
    python main.py

Cada serviço roda em um PROCESSO separado (como em uma arquitetura de
microsserviços real). Também é possível subir um serviço isolado, por exemplo:
    python -m services.catalog_service.app
"""

import subprocess
import sys

from components.database import init_database
from config import PORTS

# (nome amigável, módulo Python, chave da porta)
PROCESSOS = [
    ("Catalog Service", "services.catalog_service.app", "catalog"),
    ("Cart Service", "services.cart_service.app", "cart"),
    ("Payment Service", "services.payment_service.app", "payment"),
    ("Order Service", "services.order_service.app", "order"),
    ("Frontend", "frontend.app", "frontend"),
]


def main():
    init_database()  # cria tabelas e dados iniciais se ainda não existirem
    processos = []

    try:
        for nome, modulo, chave in PROCESSOS:
            print(f"Iniciando {nome} (porta {PORTS[chave]})...")
            processos.append(subprocess.Popen([sys.executable, "-m", modulo]))

        print(f"\nPronto! Acesse http://127.0.0.1:{PORTS['frontend']}  (Ctrl+C para encerrar)\n")
        for processo in processos:
            processo.wait()
    except KeyboardInterrupt:
        print("\nEncerrando serviços...")
    finally:
        for processo in processos:
            if processo.poll() is None:
                processo.terminate()


if __name__ == "__main__":
    main()
