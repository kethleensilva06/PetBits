"""Estado e regras da página de Prontuários."""

from typing import Optional

import reflex as rx

from petbits import models
from petbits.states.conversores import (
    formatar_data,
    formatar_data_hora,
    para_data,
    para_input_data,
)
from petbits.xano import XanoError


class ProntuarioState(rx.State):
    prontuarios: list[dict] = []
    pet_options: list[dict] = []
    funcionario_options: list[dict] = []
    search: str = ""
    load_error: str = ""

    show_dialog: bool = False
    editing_id: Optional[int] = None
    form_error: str = ""

    id_pet: str = ""
    id_funcionario: str = ""
    diagnostico: str = ""
    tratamento_realizado: str = ""
    proxima_consulta: str = ""

    def set_search(self, value: str):
        self.search = value

    def set_show_dialog(self, value: bool):
        self.show_dialog = value

    def set_id_pet(self, value: str):
        self.id_pet = value

    def set_id_funcionario(self, value: str):
        self.id_funcionario = value

    def set_diagnostico(self, value: str):
        self.diagnostico = value

    def set_tratamento_realizado(self, value: str):
        self.tratamento_realizado = value

    def set_proxima_consulta(self, value: str):
        self.proxima_consulta = value

    @rx.var
    def filtered_prontuarios(self) -> list[dict]:
        term = self.search.strip().lower()
        if not term:
            return self.prontuarios
        return [
            p
            for p in self.prontuarios
            if term in p["pet_nome"].lower() or term in p["diagnostico"].lower()
        ]

    async def load_prontuarios(self):
        self.load_error = ""
        try:
            registros = await models.prontuarios.listar()
            pets = await models.pets.listar()
            funcionarios = await models.funcionarios.listar()
        except XanoError as erro:
            self.prontuarios = []
            self.pet_options = []
            self.funcionario_options = []
            self.load_error = str(erro)
            return

        self.pet_options = [
            {"id": p.get("id"), "nome": p.get("nome") or ""}
            for p in sorted(pets, key=lambda p: (p.get("nome") or "").lower())
        ]
        self.funcionario_options = [
            {"id": f.get("id"), "nome": f.get("nome") or ""}
            for f in sorted(funcionarios, key=lambda f: (f.get("nome") or "").lower())
        ]

        pets_by_id = {p["id"]: p["nome"] for p in self.pet_options}
        funcionarios_by_id = {f["id"]: f["nome"] for f in self.funcionario_options}

        self.prontuarios = [
            {
                "id": p.get("id"),
                "pet_nome": pets_by_id.get(p.get("id_pet"), "Pet removido"),
                "funcionario_nome": funcionarios_by_id.get(
                    p.get("id_funcionario"), "Funcionário removido"
                ),
                "data_atendimento": formatar_data_hora(p.get("data_atendimento")),
                "diagnostico": p.get("diagnostico") or "-",
                "tratamento_realizado": p.get("tratamento_realizado") or "-",
                "proxima_consulta": formatar_data(p.get("proxima_consulta")),
                "proxima_consulta_input": para_input_data(p.get("proxima_consulta")),
                "id_pet": p.get("id_pet"),
                "id_funcionario": p.get("id_funcionario"),
            }
            for p in sorted(
                registros,
                key=lambda p: p.get("data_atendimento") or 0,
                reverse=True,
            )
        ]

    def open_new(self):
        self.editing_id = None
        self.id_pet = str(self.pet_options[0]["id"]) if self.pet_options else ""
        self.id_funcionario = (
            str(self.funcionario_options[0]["id"]) if self.funcionario_options else ""
        )
        self.diagnostico = ""
        self.tratamento_realizado = ""
        self.proxima_consulta = ""
        self.form_error = ""
        self.show_dialog = True

    def open_edit(self, prontuario: dict):
        self.editing_id = prontuario["id"]
        self.id_pet = str(prontuario["id_pet"])
        self.id_funcionario = str(prontuario["id_funcionario"])
        self.diagnostico = (
            prontuario["diagnostico"] if prontuario["diagnostico"] != "-" else ""
        )
        self.tratamento_realizado = (
            prontuario["tratamento_realizado"]
            if prontuario["tratamento_realizado"] != "-"
            else ""
        )
        self.proxima_consulta = prontuario["proxima_consulta_input"]
        self.form_error = ""
        self.show_dialog = True

    def close_dialog(self):
        self.show_dialog = False

    async def save(self):
        if not self.id_pet or not self.id_funcionario:
            self.form_error = "Pet e responsável pelo atendimento são obrigatórios."
            return

        dados = {
            "id_pet": int(self.id_pet),
            "id_funcionario": int(self.id_funcionario),
            "diagnostico": self.diagnostico.strip() or None,
            "tratamento_realizado": self.tratamento_realizado.strip() or None,
            "proxima_consulta": para_data(self.proxima_consulta),
        }

        try:
            if self.editing_id is None:
                await models.prontuarios.criar(dados)
            else:
                await models.prontuarios.atualizar(self.editing_id, dados)
        except XanoError as erro:
            self.form_error = str(erro)
            return

        self.form_error = ""
        self.show_dialog = False
        await self.load_prontuarios()

    async def delete(self, prontuario_id: int):
        try:
            await models.prontuarios.remover(prontuario_id)
        except XanoError as erro:
            self.load_error = str(erro)
            return
        await self.load_prontuarios()
