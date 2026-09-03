"""Estado e regras da página de Prontuários."""

from typing import Optional

import reflex as rx
from sqlmodel import select

from petbits.database import get_session
from petbits.models import Funcionario, Pet, Prontuario
from petbits.states.conversores import para_data


class ProntuarioState(rx.State):
    prontuarios: list[dict] = []
    pet_options: list[Pet] = []
    funcionario_options: list[Funcionario] = []
    search: str = ""

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

    def load_prontuarios(self):
        with get_session() as session:
            prontuarios = session.exec(
                select(Prontuario).order_by(Prontuario.data_atendimento.desc())
            ).all()
            self.pet_options = list(session.exec(select(Pet).order_by(Pet.nome)).all())
            self.funcionario_options = list(
                session.exec(select(Funcionario).order_by(Funcionario.nome)).all()
            )

        pets_by_id = {p.id: p.nome for p in self.pet_options}
        funcionarios_by_id = {f.id: f.nome for f in self.funcionario_options}

        self.prontuarios = [
            {
                "id": p.id,
                "pet_nome": pets_by_id.get(p.id_pet, "Pet removido"),
                "funcionario_nome": funcionarios_by_id.get(
                    p.id_funcionario, "Funcionário removido"
                ),
                "data_atendimento": p.data_atendimento.strftime("%d/%m/%Y %H:%M"),
                "diagnostico": p.diagnostico or "-",
                "tratamento_realizado": p.tratamento_realizado or "-",
                "proxima_consulta": (
                    p.proxima_consulta.strftime("%d/%m/%Y") if p.proxima_consulta else "-"
                ),
                "id_pet": p.id_pet,
                "id_funcionario": p.id_funcionario,
            }
            for p in prontuarios
        ]

    def open_new(self):
        self.editing_id = None
        self.id_pet = str(self.pet_options[0].id) if self.pet_options else ""
        self.id_funcionario = (
            str(self.funcionario_options[0].id) if self.funcionario_options else ""
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
        with get_session() as session:
            full = session.get(Prontuario, prontuario["id"])
            self.diagnostico = (full.diagnostico or "") if full else ""
            self.tratamento_realizado = (full.tratamento_realizado or "") if full else ""
            self.proxima_consulta = (
                full.proxima_consulta.isoformat() if full and full.proxima_consulta else ""
            )
        self.form_error = ""
        self.show_dialog = True

    def close_dialog(self):
        self.show_dialog = False

    def save(self):
        if not self.id_pet or not self.id_funcionario:
            self.form_error = "Pet e responsável pelo atendimento são obrigatórios."
            return

        with get_session() as session:
            if self.editing_id is None:
                session.add(
                    Prontuario(
                        id_pet=int(self.id_pet),
                        id_funcionario=int(self.id_funcionario),
                        diagnostico=self.diagnostico.strip() or None,
                        tratamento_realizado=self.tratamento_realizado.strip() or None,
                        proxima_consulta=para_data(self.proxima_consulta),
                    )
                )
            else:
                prontuario = session.get(Prontuario, self.editing_id)
                prontuario.id_pet = int(self.id_pet)
                prontuario.id_funcionario = int(self.id_funcionario)
                prontuario.diagnostico = self.diagnostico.strip() or None
                prontuario.tratamento_realizado = self.tratamento_realizado.strip() or None
                prontuario.proxima_consulta = para_data(self.proxima_consulta)
                session.add(prontuario)
            session.commit()

        self.show_dialog = False
        self.load_prontuarios()

    def delete(self, prontuario_id: int):
        with get_session() as session:
            prontuario = session.get(Prontuario, prontuario_id)
            if prontuario is not None:
                session.delete(prontuario)
                session.commit()
        self.load_prontuarios()
