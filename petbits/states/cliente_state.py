"""Estado e regras da página de Clientes."""

from typing import Optional

import reflex as rx
from sqlmodel import select

from petbits.database import get_session
from petbits.models import Cliente


class ClienteState(rx.State):
    clientes: list[Cliente] = []
    search: str = ""

    show_dialog: bool = False
    editing_id: Optional[int] = None
    form_error: str = ""

    nome: str = ""
    cpf: str = ""
    email: str = ""
    telefone: str = ""
    endereco: str = ""

    def set_search(self, value: str):
        self.search = value

    def set_show_dialog(self, value: bool):
        self.show_dialog = value

    def set_nome(self, value: str):
        self.nome = value

    def set_cpf(self, value: str):
        self.cpf = value

    def set_email(self, value: str):
        self.email = value

    def set_telefone(self, value: str):
        self.telefone = value

    def set_endereco(self, value: str):
        self.endereco = value

    @rx.var
    def filtered_clientes(self) -> list[Cliente]:
        term = self.search.strip().lower()
        if not term:
            return self.clientes
        return [
            c
            for c in self.clientes
            if term in c.nome.lower() or term in c.cpf.lower()
        ]

    def load_clientes(self):
        with get_session() as session:
            self.clientes = list(
                session.exec(select(Cliente).order_by(Cliente.nome)).all()
            )

    def open_new(self):
        self.editing_id = None
        self.nome = ""
        self.cpf = ""
        self.email = ""
        self.telefone = ""
        self.endereco = ""
        self.form_error = ""
        self.show_dialog = True

    def open_edit(self, cliente: Cliente):
        self.editing_id = cliente.id
        self.nome = cliente.nome
        self.cpf = cliente.cpf
        self.email = cliente.email or ""
        self.telefone = cliente.telefone or ""
        self.endereco = cliente.endereco or ""
        self.form_error = ""
        self.show_dialog = True

    def close_dialog(self):
        self.show_dialog = False

    def save(self):
        if not self.nome.strip() or not self.cpf.strip():
            self.form_error = "Nome e CPF são obrigatórios."
            return

        with get_session() as session:
            if self.editing_id is None:
                session.add(
                    Cliente(
                        nome=self.nome.strip(),
                        cpf=self.cpf.strip(),
                        email=self.email.strip() or None,
                        telefone=self.telefone.strip() or None,
                        endereco=self.endereco.strip() or None,
                    )
                )
            else:
                cliente = session.get(Cliente, self.editing_id)
                cliente.nome = self.nome.strip()
                cliente.cpf = self.cpf.strip()
                cliente.email = self.email.strip() or None
                cliente.telefone = self.telefone.strip() or None
                cliente.endereco = self.endereco.strip() or None
                session.add(cliente)
            session.commit()

        self.show_dialog = False
        self.load_clientes()

    def delete(self, cliente_id: int):
        with get_session() as session:
            cliente = session.get(Cliente, cliente_id)
            if cliente is not None:
                session.delete(cliente)
                session.commit()
        self.load_clientes()
