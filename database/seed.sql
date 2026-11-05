-- Dados iniciais do catálogo (mesmos produtos do antigo produtos.json).
-- INSERT OR IGNORE torna o script seguro para rodar mais de uma vez.

INSERT OR IGNORE INTO products (id, name, description, price, image) VALUES
    (1, 'Fone Gamer',    'Fone gamer com áudio imersivo e conforto para longas sessões.',                 200.0,  'img_prod/fone.jpg'),
    (2, 'Mouse Gamer',   'Mouse para jogo com precisão e resposta rápida para partidas competitivas.',    170.0,  'img_prod/mouse.jpg'),
    (3, 'Teclado Gamer', 'Teclado gamer com layout confortável e iluminação visual moderna.',             250.0,  'img_prod/teclado.jpg'),
    (4, 'Celular',       'Celular equilibrado para uso diário, comunicação e produtividade.',             1850.0, 'img_prod/celular.jpg'),
    (5, 'Notebook',      'Notebook para estudos, trabalho e uso geral com bom desempenho.',               3000.0, 'img_prod/notebook.jpg');
