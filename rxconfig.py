import reflex as rx

config = rx.Config(
    app_name="petbits",
    # O Radix explícito tira o aviso de habilitação implícita que o Reflex
    # dá a cada compilação (change `acabamentos`).
    plugins=[rx.plugins.SitemapPlugin(), rx.plugins.RadixThemesPlugin()],
    # Desde o Reflex 0.11 o servidor só aceita a conexão de eventos vinda do
    # próprio endereço. O site é servido de outros endereços, então eles são
    # listados aqui (change `origens-do-servidor`). Endereço novo do site
    # precisa entrar nesta lista, senão a página não conecta.
    cors_allowed_origins=[
        "https://petbits-blue-grass.reflex.run",
        "https://kethleensilva06.github.io",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
)
