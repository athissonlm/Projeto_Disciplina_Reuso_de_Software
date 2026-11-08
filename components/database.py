"""Componente: Banco de dados (SQLite).

Interface (contrato):  IDatabase
Implementação:         SQLiteDatabase

Operações:
    init_database(reset=False)   -> cria tabelas e dados iniciais (idempotente)
    ensure_database()            -> cria o banco apenas se o arquivo não existir
    connection()                 -> context manager com commit/rollback automático
    query_all(sql, params)       -> lista de dicts
    query_one(sql, params)       -> um dict (ou None)
    execute(sql, params)         -> executa INSERT/UPDATE/DELETE e devolve o último id

O módulo também expõe atalhos em forma de função, ligados a uma instância
padrão que usa os caminhos de config.py (banco da aplicação ativa).
"""

import sqlite3
from abc import ABC, abstractmethod
from contextlib import contextmanager

from config import DB_PATH, SCHEMA_PATH, SEED_PATH


class IDatabase(ABC):
    """Interface do componente de banco de dados."""

    @abstractmethod
    def connection(self):
        """Context manager que entrega uma conexão (commit/rollback automático)."""

    @abstractmethod
    def query_all(self, sql, params=()):
        """Executa um SELECT e devolve uma lista de dicts."""

    @abstractmethod
    def query_one(self, sql, params=()):
        """Executa um SELECT e devolve um dict (ou None)."""

    @abstractmethod
    def execute(self, sql, params=()):
        """Executa INSERT/UPDATE/DELETE e devolve o último id inserido."""

    @abstractmethod
    def init_database(self, reset=False):
        """Cria as tabelas e os dados iniciais."""

    @abstractmethod
    def ensure_database(self):
        """Cria o banco apenas se ele ainda não existir."""


class SQLiteDatabase(IDatabase):
    def __init__(self, db_path, schema_path, seed_path):
        self.db_path = db_path
        self.schema_path = schema_path
        self.seed_path = seed_path

    @contextmanager
    def connection(self):
        """Abre uma conexão; faz commit se tudo der certo e rollback se der erro."""
        conn = sqlite3.connect(self.db_path, timeout=10)
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

    def query_all(self, sql, params=()):
        with self.connection() as conn:
            return [dict(row) for row in conn.execute(sql, params).fetchall()]

    def query_one(self, sql, params=()):
        with self.connection() as conn:
            row = conn.execute(sql, params).fetchone()
            return dict(row) if row else None

    def execute(self, sql, params=()):
        with self.connection() as conn:
            return conn.execute(sql, params).lastrowid

    def init_database(self, reset=False):
        """Cria as tabelas (schema.sql) e insere os dados iniciais (seed.sql da aplicação)."""
        if reset and self.db_path.exists():
            self.db_path.unlink()

        with self.connection() as conn:
            conn.executescript(self.schema_path.read_text(encoding="utf-8"))
            conn.executescript(self.seed_path.read_text(encoding="utf-8"))

    def ensure_database(self):
        if not self.db_path.exists():
            self.init_database()


# Instância padrão + atalhos em forma de função
_padrao = SQLiteDatabase(DB_PATH, SCHEMA_PATH, SEED_PATH)
connection = _padrao.connection
query_all = _padrao.query_all
query_one = _padrao.query_one
execute = _padrao.execute
init_database = _padrao.init_database
ensure_database = _padrao.ensure_database
