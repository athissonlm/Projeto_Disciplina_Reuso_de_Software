"""FRAMEWORK de e-commerce.

Reúne o que é comum a qualquer loja virtual e deixa PONTOS DE ADAPTAÇÃO
(hotspots) para cada aplicação preencher:

    application.py       -> EcommerceApplication: a classe do framework (hotspots da aplicação)
    fluxo_de_compra.py   -> FluxoDeCompra: o CONTROLE da compra (padrão Template Method)
    loader.py            -> carrega a aplicação ativa (apps/<nome>/application.py)

Uma aplicação nova só precisa herdar essas classes e sobrescrever os hotspots
(veja docs/relatorio.md, seção "Como criar uma nova aplicação").
"""
