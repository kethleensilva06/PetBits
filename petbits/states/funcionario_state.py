"""Estado e regras da página de Funcionários."""

from typing import Optional

import reflex as rx

from petbits import models
from petbits.states.conversores import formatar_data, para_data, para_input_data
from petbits.xano import XanoError


class FuncionarioState(rx.State):
    funcionarios: list[dict] = []
    search: str = ""
    load_error: str = ""

    show_dialog: bool = False
    editing_id: Optional[int] = None
    form_error: str = ""

    nome: str = ""
    cpf: str = ""
    cargo: str = models.CARGOS_FUNCIONARIO[0]
    telefone: str = ""
    email: str = ""
    data_contratacao: str = ""

    def set_search(self, value: str):
        self.search = value

    def set_show_dialog(self, value: bool):
        self.show_dialog = value

    def set_nome(self, value: str):
        self.nome = value

    def set_cpf(self, value: str):
        self.cpf = value

    def set_cargo(self, value: str):
        self.cargo = value

    def set_telefone(self, value: str):
        self.telefone = value

    def set_email(self, value: str):
        self.email = value

    def set_data_contratacao(self, value: str):
        self.data_contratacao = value

    @rx.var
    def filtered_funcionarios(self) -> list[dict]:
        term = self.search.strip().lower()
        if not term:
            return self.funcionarios
        return [
            f
            for f in self.funcionarios
            if term in f["nome"].lower() or term in f["cargo"].lower()
        ]

    async def load_funcionarios(self):
        self.load_error = ""
        try:
            registros = await models.funcionarios.listar()
        except XanoError as erro:
            self.funcionarios = []
            self.load_error = str(erro)
            return

        self.funcionarios = [
            {
                "id": f.get("id"),
                "nome": f.get("nome") or "",
                "cpf": f.get("cpf") or "",
                "cargo": f.get("cargo") or "",
                "telefone": f.get("telefone") or "-",
                "email": f.get("email") or "-",
                "data_contratacao": formatar_data(f.get("data_contratacao")),
                "data_contratacao_input": para_input_data(f.get("data_contratacao")),
            }
            for f in sorted(registros, key=lambda f: (f.get("nome") or "").lower())
        ]

    def open_new(self):
        self.editing_id = None
        self.nome = ""
        self.cpf = ""
        self.cargo = models.CARGOS_FUNCIONARIO[0]
        self.telefone = ""
        self.email = ""
        self.data_contratacao = ""
        self.form_error = ""
        self.show_dialog = True

    def open_edit(self, funcionario: dict):
        self.editing_id = funcionario["id"]
        self.nome = funcionario["nome"]
        self.cpf = funcionario["cpf"]
        self.cargo = funcionario["cargo"]
        self.telefone = (
            funcionario["telefone"] if funcionario["telefone"] != "-" else ""
        )
        self.email = funcionario["email"] if funcionario["email"] != "-" else ""
        self.data_contratacao = funcionario["data_contratacao_input"]
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
            "cargo": self.cargo,
            "telefone": self.telefone.strip() or None,
            "email": self.email.strip() or None,
            "data_contratacao": para_data(self.data_contratacao),
        }

        try:
            if self.editing_id is None:
                await models.funcionarios.criar(dados)
            else:
                await models.funcionarios.atualizar(self.editing_id, dados)
        except XanoError as erro:
            self.form_error = str(erro)
            return

        self.form_error = ""
        self.show_dialog = False
        await self.load_funcionarios()

    async def delete(self, funcionario_id: int):
        try:
            await models.funcionarios.remover(funcionario_id)
        except XanoError as erro:
            self.load_error = str(erro)
            return
        await self.load_funcionarios()
