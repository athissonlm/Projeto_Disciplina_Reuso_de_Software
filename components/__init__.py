"""COMPONENTES DE SOFTWARE reutilizáveis do framework de e-commerce.

Um componente aqui é um módulo pequeno, com uma responsabilidade única e
uma INTERFACE pública (classe abstrata "I...") implementada por uma classe
concreta. Ele NÃO conhece nenhum microsserviço específico, por isso pode ser
reaproveitado por qualquer um deles (reuso).

Componente          Interface          Implementação(ões)
------------------  -----------------  -----------------------------
errors              -                  AppError, ValidationError, NotFoundError
validation          IValidador         Validador
sorting             ISorter            BubbleSorter
search              ISearcher          LinearSearcher, BinarySearcher
pricing             IPriceCalculator   PriceCalculator
database            IDatabase          SQLiteDatabase
http_client         IHttpClient        HttpClient
service_app         IServiceFactory    ServiceAppFactory

Cada módulo também oferece atalhos em forma de função (ex.: bubble_sort,
query_all, http_client.get) para uso simples.
"""
