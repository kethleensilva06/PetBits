import os

import reflex as rx

# Banco local (SQLite) por padrão. Para apontar para o SQL Server da disciplina,
# defina a variável de ambiente DB_URL, por exemplo:
# mssql+pyodbc://usuario:senha@servidor/Petshop_DQL?driver=ODBC+Driver+17+for+SQL+Server
DB_URL = os.getenv("DB_URL", "sqlite:///petbits.db")

config = rx.Config(
    app_name="petbits",
    db_url=DB_URL,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(
            theme=rx.theme(appearance="light", accent_color="teal", radius="large")
        ),
    ],
)