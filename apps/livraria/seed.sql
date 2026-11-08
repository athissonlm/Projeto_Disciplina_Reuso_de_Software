-- Dados iniciais do catálogo da LIVRARIA ONLINE (exemplos didáticos).
-- Sem imagem: o frontend usa img/placeholder.svg.
-- O "Marcador de Página" (R$ 8,00) existe para demonstrar a regra de pedido mínimo (R$ 20,00).

INSERT INTO products (id, name, description, price, image) VALUES
    (1, 'Padrões de Projeto',      'Soluções reutilizáveis para problemas comuns de design orientado a objetos.', 120.0, NULL),
    (2, 'Clean Code',              'Boas práticas para escrever código legível e fácil de manter.',               95.0,  NULL),
    (3, 'Python Fluente',          'Guia aprofundado da linguagem Python para quem já programa.',                 140.0, NULL),
    (4, 'Redes de Computadores',   'Fundamentos de redes, protocolos e arquitetura da internet.',                 160.0, NULL),
    (5, 'Sistemas Digitais',       'Lógica combinacional e sequencial, FSMs e projeto de circuitos digitais.',    110.0, NULL),
    (6, 'Marcador de Página',      'Marcador de página simples para acompanhar a leitura.',                       8.0,   NULL)
ON CONFLICT (id) DO UPDATE SET
    name        = excluded.name,
    description = excluded.description,
    price       = excluded.price,
    image       = excluded.image;
