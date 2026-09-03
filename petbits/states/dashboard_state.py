"""Estado da página inicial: indicadores e próximos agendamentos."""

from datetime import datetime

import reflex as rx
from sqlmodel import select

from petbits.database import get_session
from petbits.models import (
    Agendamento,
    Cliente,
    Funcionario,
    Pedido,
    Pet,
    Produto,
    Servico,
)


class DashboardState(rx.State):
    total_clientes: int = 0
    total_pets: int = 0
    total_funcionarios: int = 0
    total_produtos: int = 0
    total_servicos: int = 0
    agendamentos_hoje: int = 0
    pedidos_pendentes: int = 0
    proximos_agendamentos: list[dict] = []

    def load_dashboard(self):
        with get_session() as session:
            clientes = session.exec(select(Cliente)).all()
            pets = session.exec(select(Pet)).all()
            funcionarios = session.exec(select(Funcionario)).all()
            produtos = session.exec(select(Produto)).all()
            servicos = session.exec(select(Servico)).all()
            pedidos = session.exec(select(Pedido)).all()
            agendamentos = session.exec(
                select(Agendamento).order_by(Agendamento.data_hora)
            ).all()

            pets_by_id = {p.id: p.nome for p in pets}
            servicos_by_id = {s.id: s.nome_servico for s in servicos}
            funcionarios_by_id = {f.id: f.nome for f in funcionarios}

        hoje = datetime.now().date()
        agora = datetime.now()

        self.total_clientes = len(clientes)
        self.total_pets = len(pets)
        self.total_funcionarios = len(funcionarios)
        self.total_produtos = len(produtos)
        self.total_servicos = len(servicos)
        self.agendamentos_hoje = len(
            [a for a in agendamentos if a.data_hora.date() == hoje]
        )
        self.pedidos_pendentes = len([p for p in pedidos if p.status == "pendente"])

        self.proximos_agendamentos = [
            {
                "id": a.id,
                "pet_nome": pets_by_id.get(a.id_pet, "Pet removido"),
                "servico_nome": servicos_by_id.get(a.id_servico, "Serviço removido"),
                "funcionario_nome": funcionarios_by_id.get(
                    a.id_funcionario, "Funcionário removido"
                ),
                "data_hora": a.data_hora.strftime("%d/%m/%Y %H:%M"),
                "status": a.status,
            }
            for a in agendamentos
            if a.data_hora >= agora and a.status in ("agendado", "em_andamento")
        ][:8]
