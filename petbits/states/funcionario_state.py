"""Estado e regras da página de Funcionários."""

from typing import Optional

import reflex as rx
from sqlmodel import select

from petbits.database import get_session
from petbits.models import CARGOS_FUNCIONARIO, Funcionario
from petbits.states.conversores import para_data


class FuncionarioState(rx.State):
    funcionarios: list[Funcionario] = []
    search: str = ""

    show_dialog: bool = False
    editing_id: Optional[int] = None
    form_error: str = ""

    nome: str = ""
    cpf: str = ""
    cargo: str = CARGOS_FUNCIONARIO[0]
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
    def filtered_funcionarios(self) -> list[Funcionario]:
        term = self.search.strip().lower()
        if not term:
            return self.funcionarios
        return [
            f
            for f in self.funcionarios
            if term in f.nome.lower() or term in f.cargo.lower()
        ]

    def load_funcionarios(self):
        with get_session() as session:
            self.funcionarios = list(
                session.exec(select(Funcionario).order_by(Funcionario.nome)).all()
            )

    def open_new(self):
        self.editing_id = None
        self.nome = ""
        self.cpf = ""
        self.cargo = CARGOS_FUNCIONARIO[0]
        self.telefone = ""
        self.email = ""
        self.data_contratacao = ""
        self.form_error = ""
        self.show_dialog = True

    def open_edit(self, funcionario: Funcionario):
        self.editing_id = funcionario.id
        self.nome = funcionario.nome
        self.cpf = funcionario.cpf
        self.cargo = funcionario.cargo
        self.telefone = funcionario.telefone or ""
        self.email = funcionario.email or ""
        self.data_contratacao = (
            funcionario.data_contratacao.isoformat()
            if funcionario.data_contratacao
            else ""
        )
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
                    Funcionario(
                        nome=self.nome.strip(),
                        cpf=self.cpf.strip(),
                        cargo=self.cargo,
                        telefone=self.telefone.strip() or None,
                        email=self.email.strip() or None,
                        data_contratacao=para_data(self.data_contratacao),
                    )
                )
            else:
                funcionario = session.get(Funcionario, self.editing_id)
                funcionario.nome = self.nome.strip()
                funcionario.cpf = self.cpf.strip()
                funcionario.cargo = self.cargo
                funcionario.telefone = self.telefone.strip() or None
                funcionario.email = self.email.strip() or None
                funcionario.data_contratacao = para_data(self.data_contratacao)
                session.add(funcionario)
            session.commit()

        self.show_dialog = False
        self.load_funcionarios()

    def delete(self, funcionario_id: int):
        with get_session() as session:
            funcionario = session.get(Funcionario, funcionario_id)
            if funcionario is not None:
                session.delete(funcionario)
                session.commit()
        self.load_funcionarios()
