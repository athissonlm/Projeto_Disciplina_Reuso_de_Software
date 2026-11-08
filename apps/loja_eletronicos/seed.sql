-- Dados iniciais do catálogo da LOJA DE ELETRÔNICOS.
-- Usa "upsert" (INSERT ... ON CONFLICT DO UPDATE): seguro para rodar mais de uma vez.
-- Os caminhos de imagem são relativos a frontend/static/.

INSERT INTO products (id, name, description, price, image) VALUES
    (1, 'Fone Gamer',    'Fone gamer com áudio imersivo e conforto para longas sessões.',                 200.0,  'img/fone_gamer.jpg'),
    (2, 'Mouse Gamer',   'Mouse para jogo com precisão e resposta rápida para partidas competitivas.',    170.0,  'img/mouse_gamer.jpg'),
    (3, 'Teclado Gamer', 'Teclado gamer com layout confortável e iluminação visual moderna.',             250.0,  'img/teclado_gamer.jpg'),
    (4, 'Celular',       'Celular equilibrado para uso diário, comunicação e produtividade.',             1850.0, 'img/celular.jpg'),
    (5, 'Notebook',      'Notebook para estudos, trabalho e uso geral com bom desempenho.',               3000.0, 'img/notebook.jpg')
ON CONFLICT (id) DO UPDATE SET
    name        = excluded.name,
    description = excluded.description,
    price       = excluded.price,
    image       = excluded.image;
