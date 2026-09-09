"""Estado e regras da página de Clientes."""

from typing import Optional

import reflex as rx

from petbits import models
from petbits.xano import XanoError


class ClienteState(rx.State):
    clientes: list[dict] = []
    search: str = ""
    load_error: str = ""

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
    def filtered_clientes(self) -> list[dict]:
        term = self.search.strip().lower()
        if not term:
            return self.clientes
        return [
            c
            for c in self.clientes
            if term in c["nome"].lower() or term in c["cpf"].lower()
        ]

    async def load_clientes(self):
        self.load_error = ""
        try:
            registros = await models.clientes.listar()
        except XanoError as erro:
            self.clientes = []
            self.load_error = str(erro)
            return

        self.clientes = [
            {
                "id": c.get("id"),
                "nome": c.get("nome") or "",
                "cpf": c.get("cpf") or "",
                "email": c.get("email") or "-",
                "telefone": c.get("telefone") or "-",
                "endereco": c.get("endereco") or "-",
            }
            for c in sorted(registros, key=lambda c: (c.get("nome") or "").lower())
        ]

    def open_new(self):
        self.editing_id = None
        self.nome = ""
        self.cpf = ""
        self.email = ""
        self.telefone = ""
        self.endereco = ""
        self.form_error = ""
        self.show_dialog = True

    def open_edit(self, cliente: dict):
        self.editing_id = cliente["id"]
        self.nome = cliente["nome"]
        self.cpf = cliente["cpf"]
        self.email = cliente["email"] if cliente["email"] != "-" else ""
        self.telefone = cliente["telefone"] if cliente["telefone"] != "-" else ""
        self.endereco = cliente["endereco"] if cliente["endereco"] != "-" else ""
        self.form_error = ""
        self.show_dialog = True

    def close_dialog(self):
        self.show_dialog = False

    async def save(self):
        if not self.nome.strip() or not self.cpf.strip():
            self.form_error = "Nome e CPF são obrigatórios."
            return

        dados = {
            "nome": self.nome.strip(),
            "cpf": self.cpf.strip(),
            "email": self.email.strip() or None,
            "telefone": self.telefone.strip() or None,
            "endereco": self.endereco.strip() or None,
        }

        try:
            if self.editing_id is None:
                await models.clientes.criar(dados)
            else:
                await models.clientes.atualizar(self.editing_id, dados)
        except XanoError as erro:
            self.form_error = str(erro)
            return

        self.form_error = ""
        self.show_dialog = False
        await self.load_clientes()

    async def delete(self, cliente_id: int):
        try:
            await models.clientes.remover(cliente_id)
        except XanoError as erro:
            self.load_error = str(erro)
            return
        await self.load_clientes()
