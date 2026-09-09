import reflex as rx

# O banco de dados do PetBits fica no Xano e é acessado por HTTP
# (petbits/xano.py). O Reflex, portanto, não recebe db_url: nada neste projeto
# usa o ORM interno dele. As credenciais do Xano vêm do arquivo .env.
config = rx.Config(
    app_name="petbits",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(
            theme=rx.theme(appearance="light", accent_color="teal", radius="large")
        ),
    ],
)
