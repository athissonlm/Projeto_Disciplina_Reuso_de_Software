"""Launcher do projeto: sobe o banco, o API Gateway, os 4 microsserviços e o frontend.

Uso:
    python main.py                     # aplicação 1: loja_eletronicos (padrão)
    python main.py --app livraria      # aplicação 2: livraria

Cada serviço roda em um PROCESSO separado (como em uma arquitetura de
microsserviços real). Também é possível subir um serviço isolado, por exemplo:
    python -m services.catalog_service.app

Rode uma aplicação por vez (as duas usam as mesmas portas).
"""

import os
import subprocess
import sys


def _escolher_aplicacao():
    """Lê --app <nome> e define ECOMMERCE_APP ANTES de importar o config (os subprocessos herdam)."""
    if "--app" in sys.argv:
        indice = sys.argv.index("--app")
        if indice + 1 >= len(sys.argv):
            sys.exit("Uso: python main.py --app <loja_eletronicos|livraria>")
        os.environ["ECOMMERCE_APP"] = sys.argv[indice + 1]


_escolher_aplicacao()

from components.database import init_database  # noqa: E402
from config import APP_NAME, PORTS  # noqa: E402

# (nome amigável, módulo Python, chave da porta)
PROCESSOS = [
    ("Catalog Service", "services.catalog_service.app", "catalog"),
    ("Cart Service", "services.cart_service.app", "cart"),
    ("Payment Service", "services.payment_service.app", "payment"),
    ("Order Service", "services.order_service.app", "order"),
    ("API Gateway", "gateway.app", "gateway"),
    ("Frontend", "frontend.app", "frontend"),
]


def main():
    print(f"Aplicação: {APP_NAME}")
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
