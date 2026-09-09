"""Estado e regras da página de Serviços."""

from typing import Optional

import reflex as rx

from petbits import models
from petbits.states.conversores import formatar_moeda
from petbits.xano import XanoError


class ServicoState(rx.State):
    servicos: list[dict] = []
    search: str = ""
    load_error: str = ""

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

    async def load_servicos(self):
        self.load_error = ""
        try:
            registros = await models.servicos.listar()
        except XanoError as erro:
            self.servicos = []
            self.load_error = str(erro)
            return

        self.servicos = [
            {
                "id": s.get("id"),
                "nome_servico": s.get("nome_servico") or "",
                "descricao": s.get("descricao") or "-",
                "preco": formatar_moeda(s.get("preco")),
                "duracao_estimada": s.get("duracao_estimada") or 0,
            }
            for s in sorted(
                registros, key=lambda s: (s.get("nome_servico") or "").lower()
            )
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

    async def save(self):
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

        dados = {
            "nome_servico": self.nome_servico.strip(),
            "descricao": self.descricao.strip() or None,
            "preco": preco,
            "duracao_estimada": duracao,
        }

        try:
            if self.editing_id is None:
                await models.servicos.criar(dados)
            else:
                await models.servicos.atualizar(self.editing_id, dados)
        except XanoError as erro:
            self.form_error = str(erro)
            return

        self.form_error = ""
        self.show_dialog = False
        await self.load_servicos()

    async def delete(self, servico_id: int):
        try:
            await models.servicos.remover(servico_id)
        except XanoError as erro:
            self.load_error = str(erro)
            return
        await self.load_servicos()
