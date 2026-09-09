"""Estado e regras da página de Agendamentos."""

from typing import Optional

import reflex as rx

from petbits import models
from petbits.states.conversores import (
    formatar_data_hora,
    para_data_hora,
    para_input_data_hora,
)
from petbits.xano import XanoError


class AgendamentoState(rx.State):
    agendamentos: list[dict] = []
    pet_options: list[dict] = []
    servico_options: list[dict] = []
    funcionario_options: list[dict] = []
    search: str = ""
    load_error: str = ""

    show_dialog: bool = False
    editing_id: Optional[int] = None
    form_error: str = ""

    id_pet: str = ""
    id_servico: str = ""
    id_funcionario: str = ""
    data_hora: str = ""
    status: str = models.STATUS_AGENDAMENTO[0]
    observacoes: str = ""

    def set_search(self, value: str):
        self.search = value

    def set_show_dialog(self, value: bool):
        self.show_dialog = value

    def set_id_pet(self, value: str):
        self.id_pet = value

    def set_id_servico(self, value: str):
        self.id_servico = value

    def set_id_funcionario(self, value: str):
        self.id_funcionario = value

    def set_data_hora(self, value: str):
        self.data_hora = value

    def set_status(self, value: str):
        self.status = value

    def set_observacoes(self, value: str):
        self.observacoes = value

    @rx.var
    def filtered_agendamentos(self) -> list[dict]:
        term = self.search.strip().lower()
        if not term:
            return self.agendamentos
        return [
            a
            for a in self.agendamentos
            if term in a["pet_nome"].lower() or term in a["servico_nome"].lower()
        ]

    async def load_agendamentos(self):
        self.load_error = ""
        try:
            registros = await models.agendamentos.listar()
            pets = await models.pets.listar()
            servicos = await models.servicos.listar()
            funcionarios = await models.funcionarios.listar()
        except XanoError as erro:
            self.agendamentos = []
            self.pet_options = []
            self.servico_options = []
            self.funcionario_options = []
            self.load_error = str(erro)
            return

        self.pet_options = [
            {"id": p.get("id"), "nome": p.get("nome") or ""}
            for p in sorted(pets, key=lambda p: (p.get("nome") or "").lower())
        ]
        self.servico_options = [
            {"id": s.get("id"), "nome_servico": s.get("nome_servico") or ""}
            for s in sorted(
                servicos, key=lambda s: (s.get("nome_servico") or "").lower()
            )
        ]
        self.funcionario_options = [
            {"id": f.get("id"), "nome": f.get("nome") or ""}
            for f in sorted(funcionarios, key=lambda f: (f.get("nome") or "").lower())
        ]

        pets_by_id = {p["id"]: p["nome"] for p in self.pet_options}
        servicos_by_id = {s["id"]: s["nome_servico"] for s in self.servico_options}
        funcionarios_by_id = {f["id"]: f["nome"] for f in self.funcionario_options}

        self.agendamentos = [
            {
                "id": a.get("id"),
                "pet_nome": pets_by_id.get(a.get("id_pet"), "Pet removido"),
                "servico_nome": servicos_by_id.get(
                    a.get("id_servico"), "Serviço removido"
                ),
                "funcionario_nome": funcionarios_by_id.get(
                    a.get("id_funcionario"), "Funcionário removido"
                ),
                "data_hora": formatar_data_hora(a.get("data_hora")),
                "status": a.get("status") or "",
                "id_pet": a.get("id_pet"),
                "id_servico": a.get("id_servico"),
                "id_funcionario": a.get("id_funcionario"),
                "data_hora_input": para_input_data_hora(a.get("data_hora")),
                "observacoes": a.get("observacoes") or "",
            }
            for a in sorted(
                registros, key=lambda a: a.get("data_hora") or 0, reverse=True
            )
        ]

    def open_new(self):
        self.editing_id = None
        self.id_pet = str(self.pet_options[0]["id"]) if self.pet_options else ""
        self.id_servico = (
            str(self.servico_options[0]["id"]) if self.servico_options else ""
        )
        self.id_funcionario = (
            str(self.funcionario_options[0]["id"]) if self.funcionario_options else ""
        )
        self.data_hora = ""
        self.status = models.STATUS_AGENDAMENTO[0]
        self.observacoes = ""
        self.form_error = ""
        self.show_dialog = True

    def open_edit(self, agendamento: dict):
        self.editing_id = agendamento["id"]
        self.id_pet = str(agendamento["id_pet"])
        self.id_servico = str(agendamento["id_servico"])
        self.id_funcionario = str(agendamento["id_funcionario"])
        self.status = agendamento["status"]
        self.data_hora = agendamento["data_hora_input"]
        self.observacoes = agendamento["observacoes"]
        self.form_error = ""
        self.show_dialog = True

    def close_dialog(self):
        self.show_dialog = False

    async def save(self):
        if not (self.id_pet and self.id_servico and self.id_funcionario and self.data_hora):
            self.form_error = "Pet, serviço, funcionário e data/hora são obrigatórios."
            return

        dados = {
            "id_pet": int(self.id_pet),
            "id_servico": int(self.id_servico),
            "id_funcionario": int(self.id_funcionario),
            "data_hora": para_data_hora(self.data_hora),
            "status": self.status,
            "observacoes": self.observacoes.strip() or None,
        }

        try:
            if self.editing_id is None:
                await models.agendamentos.criar(dados)
            else:
                await models.agendamentos.atualizar(self.editing_id, dados)
        except XanoError as erro:
            self.form_error = str(erro)
            return

        self.form_error = ""
        self.show_dialog = False
        await self.load_agendamentos()

    async def delete(self, agendamento_id: int):
        try:
            await models.agendamentos.remover(agendamento_id)
        except XanoError as erro:
            self.load_error = str(erro)
            return
        await self.load_agendamentos()
