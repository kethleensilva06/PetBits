"""Estado e regras da página de Serviços."""

from typing import Optional

import reflex as rx
from sqlmodel import select

from petbits.database import get_session
from petbits.models import Servico


class ServicoState(rx.State):
    servicos: list[dict] = []
    search: str = ""

    show_dialog: bool = False
    editing_id: Optional[int] = None
    form_error: str = ""

    nome_servico: str = ""
    descricao: str = ""
    preco: str = "0.00"
    duracao_estimada: str = "30"

    def set_search(self, value: str):
        self.search = value

    def set_show_dialog(self, value: bool):
        self.show_dialog = value

    def set_nome_servico(self, value: str):
        self.nome_servico = value

    def set_descricao(self, value: str):
        self.descricao = value

    def set_preco(self, value: str):
        self.preco = value

    def set_duracao_estimada(self, value: str):
        self.duracao_estimada = value

    @rx.var
    def filtered_servicos(self) -> list[dict]:
        term = self.search.strip().lower()
        if not term:
            return self.servicos
        return [s for s in self.servicos if term in s["nome_servico"].lower()]

    def load_servicos(self):
        with get_session() as session:
            servicos = session.exec(
                select(Servico).order_by(Servico.nome_servico)
            ).all()

        self.servicos = [
            {
                "id": s.id,
                "nome_servico": s.nome_servico,
                "descricao": s.descricao or "-",
                "preco": f"{s.preco:.2f}",
                "duracao_estimada": s.duracao_estimada or 0,
            }
            for s in servicos
        ]

    def open_new(self):
        self.editing_id = None
        self.nome_servico = ""
        self.descricao = ""
        self.preco = "0.00"
        self.duracao_estimada = "30"
        self.form_error = ""
        self.show_dialog = True

    def open_edit(self, servico: dict):
        self.editing_id = servico["id"]
        self.nome_servico = servico["nome_servico"]
        self.descricao = servico["descricao"] if servico["descricao"] != "-" else ""
        self.preco = servico["preco"]
        self.duracao_estimada = str(servico["duracao_estimada"])
        self.form_error = ""
        self.show_dialog = True

    def close_dialog(self):
        self.show_dialog = False

    def save(self):
        if not self.nome_servico.strip():
            self.form_error = "Nome do serviço é obrigatório."
            return
        try:
            preco = float(self.preco.replace(",", "."))
            duracao = int(self.duracao_estimada)
        except ValueError:
            self.form_error = "Preço ou duração inválidos."
            return
        if preco < 0:
            self.form_error = "Preço não pode ser negativo."
            return
        if duracao <= 0:
            self.form_error = "Duração deve ser maior que zero."
            return

        with get_session() as session:
            if self.editing_id is None:
                session.add(
                    Servico(
                        nome_servico=self.nome_servico.strip(),
                        descricao=self.descricao.strip() or None,
                        preco=preco,
                        duracao_estimada=duracao,
                    )
                )
            else:
                servico = session.get(Servico, self.editing_id)
                servico.nome_servico = self.nome_servico.strip()
                servico.descricao = self.descricao.strip() or None
                servico.preco = preco
                servico.duracao_estimada = duracao
                session.add(servico)
            session.commit()

        self.show_dialog = False
        self.load_servicos()

    def delete(self, servico_id: int):
        with get_session() as session:
            servico = session.get(Servico, servico_id)
            if servico is not None:
                session.delete(servico)
                session.commit()
        self.load_servicos()
