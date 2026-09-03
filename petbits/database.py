"""Conexão com o banco de dados.

Em desenvolvimento usa SQLite local. Para apontar para o SQL Server da
disciplina, defina a variável de ambiente DB_URL antes de rodar a aplicação:

    mssql+pyodbc://usuario:senha@servidor/Petshop_DQL?driver=ODBC+Driver+17+for+SQL+Server

Nesse caso as tabelas já existem no servidor e `create_db_and_tables()` não
precisa ser chamada.
"""

import os

from sqlmodel import Session, SQLModel, create_engine

from petbits import models  # noqa: F401  (registra as tabelas no metadata)

DB_URL = os.getenv("DB_URL", "sqlite:///petbits.db")

engine = create_engine(DB_URL, echo=False)


def create_db_and_tables():
    """Cria as tabelas que ainda não existem (usado no ambiente local)."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    """Abre uma sessão do banco. Use sempre dentro de um `with`."""
    return Session(engine)
