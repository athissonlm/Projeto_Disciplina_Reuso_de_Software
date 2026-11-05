-- =====================================================================
-- Esquema do banco de dados (SQLite) do framework de e-commerce
--
-- Regra didática: cada tabela pertence a UM microsserviço e só ele
-- lê/escreve nela. Por isso não existem chaves estrangeiras entre
-- tabelas de serviços diferentes (ex.: cart_items.product_id NÃO é FK
-- para products). Os serviços se comunicam por HTTP, não por JOIN.
-- =====================================================================

-- ---------------------------------------------------------------------
-- Catalog Service
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS products (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL UNIQUE,
    description TEXT,
    price       REAL    NOT NULL CHECK (price >= 0),
    image       TEXT
);

-- ---------------------------------------------------------------------
-- Cart Service
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS cart_items (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_id    TEXT    NOT NULL,
    product_id INTEGER NOT NULL,
    quantity   INTEGER NOT NULL CHECK (quantity > 0),
    UNIQUE (cart_id, product_id)
);

-- ---------------------------------------------------------------------
-- Order Service
-- status: created | paid | payment_failed
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS orders (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    total         REAL NOT NULL,
    status        TEXT NOT NULL DEFAULT 'created',
    created_at    TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- O nome e o preço do produto são copiados para o pedido (snapshot),
-- assim o histórico não muda se o catálogo for alterado depois.
CREATE TABLE IF NOT EXISTS order_items (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id     INTEGER NOT NULL REFERENCES orders (id),
    product_id   INTEGER NOT NULL,
    product_name TEXT    NOT NULL,
    unit_price   REAL    NOT NULL,
    quantity     INTEGER NOT NULL CHECK (quantity > 0)
);

-- ---------------------------------------------------------------------
-- Payment Service
-- status: approved | refused
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS payments (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id   INTEGER NOT NULL,
    amount     REAL    NOT NULL,
    method     TEXT    NOT NULL,
    status     TEXT    NOT NULL,
    message    TEXT,
    created_at TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP
);
