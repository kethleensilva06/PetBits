"""Estado e regras da página de Agendamentos."""

from typing import Optional

import reflex as rx
from sqlmodel import select

from petbits.database import get_session
from petbits.models import STATUS_AGENDAMENTO, Agendamento, Funcionario, Pet, Servico
from petbits.states.conversores import para_data_hora


class AgendamentoState(rx.State):
    agendamentos: list[dict] = []
    pet_options: list[Pet] = []
    servico_options: list[Servico] = []
    funcionario_options: list[Funcionario] = []
    search: str = ""

    show_dialog: bool = False
    editing_id: Optional[int] = None
    form_error: str = ""

    id_pet: str = ""
    id_servico: str = ""
    id_funcionario: str = ""
    data_hora: str = ""
    status: str = STATUS_AGENDAMENTO[0]
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

    def load_agendamentos(self):
        with get_session() as session:
            agendamentos = session.exec(
                select(Agendamento).order_by(Agendamento.data_hora.desc())
            ).all()
            self.pet_options = list(session.exec(select(Pet).order_by(Pet.nome)).all())
            self.servico_options = list(
                session.exec(select(Servico).order_by(Servico.nome_servico)).all()
            )
            self.funcionario_options = list(
                session.exec(select(Funcionario).order_by(Funcionario.nome)).all()
            )

        pets_by_id = {p.id: p.nome for p in self.pet_options}
        servicos_by_id = {s.id: s.nome_servico for s in self.servico_options}
        funcionarios_by_id = {f.id: f.nome for f in self.funcionario_options}

        self.agendamentos = [
            {
                "id": a.id,
                "pet_nome": pets_by_id.get(a.id_pet, "Pet removido"),
                "servico_nome": servicos_by_id.get(a.id_servico, "Serviço removido"),
                "funcionario_nome": funcionarios_by_id.get(
                    a.id_funcionario, "Funcionário removido"
                ),
                "data_hora": a.data_hora.strftime("%d/%m/%Y %H:%M"),
                "status": a.status,
                "id_pet": a.id_pet,
                "id_servico": a.id_servico,
                "id_funcionario": a.id_funcionario,
            }
            for a in agendamentos
        ]

    def open_new(self):
        self.editing_id = None
        self.id_pet = str(self.pet_options[0].id) if self.pet_options else ""
        self.id_servico = str(self.servico_options[0].id) if self.servico_options else ""
        self.id_funcionario = (
            str(self.funcionario_options[0].id) if self.funcionario_options else ""
        )
        self.data_hora = ""
        self.status = STATUS_AGENDAMENTO[0]
        self.observacoes = ""
        self.form_error = ""
        self.show_dialog = True

    def open_edit(self, agendamento: dict):
        self.editing_id = agendamento["id"]
        self.id_pet = str(agendamento["id_pet"])
        self.id_servico = str(agendamento["id_servico"])
        self.id_funcionario = str(agendamento["id_funcionario"])
        self.status = agendamento["status"]
        with get_session() as session:
            full = session.get(Agendamento, agendamento["id"])
            self.observacoes = (full.observacoes or "") if full else ""
            self.data_hora = full.data_hora.strftime("%Y-%m-%dT%H:%M") if full else ""
        self.form_error = ""
        self.show_dialog = True

    def close_dialog(self):
        self.show_dialog = False

    def save(self):
        if not (self.id_pet and self.id_servico and self.id_funcionario and self.data_hora):
            self.form_error = "Pet, serviço, funcionário e data/hora são obrigatórios."
            return

        with get_session() as session:
            if self.editing_id is None:
                session.add(
                    Agendamento(
                        id_pet=int(self.id_pet),
                        id_servico=int(self.id_servico),
                        id_funcionario=int(self.id_funcionario),
                        data_hora=para_data_hora(self.data_hora),
                        status=self.status,
                        observacoes=self.observacoes.strip() or None,
                    )
                )
            else:
                agendamento = session.get(Agendamento, self.editing_id)
                agendamento.id_pet = int(self.id_pet)
                agendamento.id_servico = int(self.id_servico)
                agendamento.id_funcionario = int(self.id_funcionario)
                agendamento.data_hora = para_data_hora(self.data_hora)
                agendamento.status = self.status
                agendamento.observacoes = self.observacoes.strip() or None
                session.add(agendamento)
            session.commit()

        self.show_dialog = False
        self.load_agendamentos()

    def delete(self, agendamento_id: int):
        with get_session() as session:
            agendamento = session.get(Agendamento, agendamento_id)
            if agendamento is not None:
                session.delete(agendamento)
                session.commit()
        self.load_agendamentos()
