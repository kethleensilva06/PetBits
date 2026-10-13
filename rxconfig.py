import reflex as rx

config = rx.Config(
    app_name="petbits",
    # O Radix explícito tira o aviso de habilitação implícita que o Reflex
    # dá a cada compilação (change `acabamentos`).
    plugins=[rx.plugins.SitemapPlugin(), rx.plugins.RadixThemesPlugin()],
)
