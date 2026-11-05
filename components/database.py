"""Componente: Banco de dados (SQLite).

Interface pública:
    init_database(reset=False)   -> cria tabelas e dados iniciais (idempotente)
    ensure_database()            -> cria o banco apenas se o arquivo não existir
    connection()                 -> context manager com commit/rollback automático
    query_all(sql, params)       -> lista de dicts
    query_one(sql, params)       -> um dict (ou None)
    execute(sql, params)         -> executa INSERT/UPDATE/DELETE e devolve o último id
"""

import sqlite3
from contextlib import contextmanager

from config import DB_PATH, SCHEMA_PATH, SEED_PATH


@contextmanager
def connection():
    """Abre uma conexão; faz commit se tudo der certo e rollback se der erro."""
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def query_all(sql, params=()):
    with connection() as conn:
        return [dict(row) for row in conn.execute(sql, params).fetchall()]


def query_one(sql, params=()):
    with connection() as conn:
        row = conn.execute(sql, params).fetchone()
        return dict(row) if row else None


def execute(sql, params=()):
    with connection() as conn:
        return conn.execute(sql, params).lastrowid


def init_database(reset=False):
    """Cria as tabelas (schema.sql) e insere os dados iniciais (seed.sql)."""
    if reset and DB_PATH.exists():
        DB_PATH.unlink()

    with connection() as conn:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        conn.executescript(SEED_PATH.read_text(encoding="utf-8"))


def ensure_database():
    if not DB_PATH.exists():
        init_database()
